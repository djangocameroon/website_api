from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            username="testuser",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpass123"))

    def test_user_str(self):
        self.assertEqual(self.user.email, "test@example.com")

    def test_user_default_fields(self):
        self.assertFalse(self.user.is_organizer)
        self.assertEqual(self.user.gender, "Male")

    def test_user_email_unique(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                email="test@example.com",
                password="otherpass",
                username="otheruser",
            )

    def test_user_profile_fields(self):
        self.user.bio = "A test bio"
        self.user.phone_number = "+237600000000"
        self.user.is_organizer = True
        self.user.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, "A test bio")
        self.assertEqual(self.user.phone_number, "+237600000000")
        self.assertTrue(self.user.is_organizer)


class LoginHistoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="history@example.com",
            password="testpass123",
            username="historyuser",
        )

    def test_is_new_login_location_first_login(self):
        from apps.users.models.login_history import LoginHistory
        self.assertTrue(
            LoginHistory.is_new_login_location(self.user, "192.168.1.1")
        )

    def test_is_not_new_after_previous_login(self):
        from apps.users.models.login_history import LoginHistory
        LoginHistory.objects.create(
            user=self.user,
            ip_address="192.168.1.1",
            login_successful=True,
        )
        self.assertFalse(
            LoginHistory.is_new_login_location(self.user, "192.168.1.1")
        )

    def test_get_location_string(self):
        from apps.users.models.login_history import LoginHistory
        self.assertEqual(
            LoginHistory.get_location_string("Cameroon", "Douala"),
            "Douala, Cameroon"
        )
        self.assertEqual(
            LoginHistory.get_location_string("Cameroon", ""),
            "Cameroon"
        )
        self.assertEqual(
            LoginHistory.get_location_string("", ""),
            "Unknown location"
        )
