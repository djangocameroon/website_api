from unittest.mock import patch

from django.core import mail
from django.core.cache import cache
from django.test import TestCase
from django.utils.timezone import now, timedelta
from rest_framework import status
from rest_framework.test import APIClient

from apps.subs.models import Subscriber, SubscriptionVerificationToken
from apps.subs.services import SubscriberUnsubscribeService, SubscriptionVerificationService


class SubscriptionVerificationServiceTest(TestCase):
    def setUp(self):
        self.service = SubscriptionVerificationService()
        self.email = "reader@example.com"

    def test_generate_token_creates_token_for_email(self):
        token = self.service.generate_token(self.email)
        token_obj = SubscriptionVerificationToken.objects.get(token=token)
        self.assertEqual(token_obj.email, self.email)
        self.assertFalse(token_obj.has_expired())

    def test_generate_token_invalidates_previous_tokens(self):
        first_token = self.service.generate_token(self.email)
        self.service.generate_token(self.email)
        self.assertFalse(SubscriptionVerificationToken.objects.filter(token=first_token).exists())
        self.assertEqual(SubscriptionVerificationToken.objects.filter(email=self.email).count(), 1)

    def test_verify_token_creates_verified_subscriber(self):
        token = self.service.generate_token(self.email)
        result_email = self.service.verify_token(token)

        self.assertEqual(result_email, self.email)
        subscriber = Subscriber.objects.get(email=self.email)
        self.assertTrue(subscriber.is_verified)

    def test_verify_token_invalidates_token_after_use(self):
        token = self.service.generate_token(self.email)
        self.service.verify_token(token)

        self.assertFalse(SubscriptionVerificationToken.objects.filter(token=token).exists())
        self.assertIsNone(self.service.verify_token(token))

    def test_verify_token_returns_none_for_unknown_token(self):
        self.assertIsNone(self.service.verify_token("does-not-exist"))

    def test_verify_token_returns_none_and_deletes_expired_token(self):
        token_obj = SubscriptionVerificationToken.objects.create(
            email=self.email, expires_at=now() - timedelta(hours=1)
        )
        self.assertIsNone(self.service.verify_token(token_obj.token))
        self.assertFalse(SubscriptionVerificationToken.objects.filter(pk=token_obj.pk).exists())

    def test_send_verification_email_sends_mail_with_link(self):
        self.service.send_verification_email(self.email)

        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        self.assertEqual(sent.to, [self.email])

        token = SubscriptionVerificationToken.objects.get(email=self.email).token
        self.assertIn(token, sent.body)


class SendSubscriptionVerificationViewTest(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.url = "/api/v1/subscribers/verify/send/"

    @patch("apps.subs.views.send_subscription_verification_email_task.delay")
    def test_sends_verification_email_for_new_email(self, mock_delay):
        response = self.client.post(self.url, {"email": "new@example.com"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_delay.assert_called_once_with("new@example.com")
        self.assertFalse(Subscriber.objects.filter(email="new@example.com").exists())

    @patch("apps.subs.views.send_subscription_verification_email_task.delay")
    def test_does_not_resend_for_already_verified_email(self, mock_delay):
        Subscriber.objects.create(email="verified@example.com", is_verified=True)

        response = self.client.post(self.url, {"email": "verified@example.com"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_delay.assert_not_called()


class VerifySubscriptionEmailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/subscribers/verify/"
        self.service = SubscriptionVerificationService()

    def test_verifies_valid_token(self):
        token = self.service.generate_token("confirm@example.com")

        response = self.client.post(self.url, {"token": token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscriber.objects.filter(email="confirm@example.com", is_verified=True).exists()
        )

    def test_rejects_invalid_token(self):
        response = self.client.post(self.url, {"token": "bogus-token"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SubscriberUnsubscribeServiceTest(TestCase):
    def setUp(self):
        self.service = SubscriberUnsubscribeService()
        self.subscriber = Subscriber.objects.create(email="leaving@example.com", is_verified=True)

    def test_unsubscribe_deletes_subscriber_and_returns_email(self):
        email = self.service.unsubscribe(self.subscriber.unsubscribe_token)

        self.assertEqual(email, "leaving@example.com")
        self.assertFalse(Subscriber.objects.filter(pk=self.subscriber.pk).exists())

    def test_unsubscribe_returns_none_for_unknown_token(self):
        self.assertIsNone(self.service.unsubscribe("bogus-token"))
        self.assertTrue(Subscriber.objects.filter(pk=self.subscriber.pk).exists())


class UnsubscribeViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/subscribers/unsubscribe/"
        self.subscriber = Subscriber.objects.create(email="leaving2@example.com", is_verified=True)

    def test_unsubscribes_with_valid_token(self):
        response = self.client.post(self.url, {"token": self.subscriber.unsubscribe_token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscriber.objects.filter(pk=self.subscriber.pk).exists())

    def test_rejects_invalid_unsubscribe_token(self):
        response = self.client.post(self.url, {"token": "bogus-token"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(Subscriber.objects.filter(pk=self.subscriber.pk).exists())
