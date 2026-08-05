from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import now, timedelta

from apps.events.models.event import Event, EventCity, EventRegion, EventVenue
from apps.events.models.event_registration import EventRegistration
from apps.events.models.projects import Project
from apps.events.models.reservation import Reservation
from apps.events.models.speaker import Speaker

User = get_user_model()


class SpeakerModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(name="Alice Speaker")

    def test_speaker_creation(self):
        self.assertEqual(self.speaker.name, "Alice Speaker")
        self.assertTrue(self.speaker.active)

    def test_speaker_auto_slug(self):
        self.assertEqual(self.speaker.slug, "alice-speaker")

    def test_speaker_str(self):
        self.assertEqual(str(self.speaker), "Alice Speaker")


class EventModelTest(TestCase):
    def setUp(self):
        self.region = EventRegion.objects.create(name="Centre")
        self.city = EventCity.objects.create(name="Douala", region=self.region)
        self.venue = EventVenue.objects.create(name="Tech Hub", city=self.city)
        self.event = Event.objects.create(
            title="Django Meetup",
            description="Monthly meetup",
            location=self.venue,
            date=now() + timedelta(days=7),
            type="In-person",
            category="Workshops",
        )

    def test_event_creation(self):
        self.assertEqual(self.event.title, "Django Meetup")

    def test_event_str(self):
        self.assertEqual(str(self.event), "Django Meetup")

    def test_event_slug_generated(self):
        self.assertIsNotNone(self.event.slug)


class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="reserve@example.com",
            password="testpass123",
            username="reserveuser",
        )
        region = EventRegion.objects.create(name="Littoral")
        city = EventCity.objects.create(name="Douala", region=region)
        venue = EventVenue.objects.create(name="Venue", city=city)
        self.event = Event.objects.create(
            title="Test Event",
            description="Desc",
            location=venue,
            date=now() + timedelta(days=3),
            type="Online",
            category="Talks",
        )

    def test_reservation_creation(self):
        reservation = Reservation.objects.create(
            for_event=self.event,
            user=self.user,
        )
        self.assertFalse(reservation.check_in)

    def test_reservation_unique_per_event_user(self):
        Reservation.objects.create(for_event=self.event, user=self.user)
        with self.assertRaises(Exception):
            Reservation.objects.create(for_event=self.event, user=self.user)

    def test_reservation_str(self):
        reservation = Reservation.objects.create(
            for_event=self.event, user=self.user
        )
        self.assertIn(self.user.email, str(reservation))

    def test_reservation_blocked_when_event_has_external_registration_link(self):
        self.event.external_registration_link = "https://example.com/register"
        self.event.save()
        with self.assertRaises(ValidationError):
            Reservation.objects.create(for_event=self.event, user=self.user)

    def test_reservation_allowed_when_external_registration_link_is_empty_string(self):
        self.event.external_registration_link = ""
        self.event.save()
        reservation = Reservation.objects.create(for_event=self.event, user=self.user)
        self.assertFalse(reservation.check_in)


class EventRegistrationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="reg@example.com",
            password="testpass123",
            username="reguser",
        )
        region = EventRegion.objects.create(name="Centre")
        city = EventCity.objects.create(name="Yaounde", region=region)
        venue = EventVenue.objects.create(name="Arena", city=city)
        self.event = Event.objects.create(
            title="Registration Event",
            description="Desc",
            location=venue,
            date=now() + timedelta(days=5),
            type="Hybrid",
            category="Talks",
        )

    def test_registration_code_auto_generated(self):
        reg = EventRegistration.objects.create(
            event=self.event, user=self.user
        )
        self.assertTrue(reg.registration_code.startswith("REG-"))
        self.assertEqual(len(reg.registration_code), 12)

    def test_registration_default_status(self):
        reg = EventRegistration.objects.create(
            event=self.event, user=self.user
        )
        self.assertEqual(reg.status, "registered")

    def test_mark_as_attended(self):
        reg = EventRegistration.objects.create(
            event=self.event, user=self.user
        )
        reg.mark_as_attended()
        reg.refresh_from_db()
        self.assertEqual(reg.status, "attended")
        self.assertTrue(reg.checked_in)
        self.assertIsNotNone(reg.check_in_time)

    def test_cancel_registration(self):
        reg = EventRegistration.objects.create(
            event=self.event, user=self.user
        )
        reg.cancel_registration()
        reg.refresh_from_db()
        self.assertEqual(reg.status, "cancelled")


class ProjectModelTest(TestCase):
    def test_project_creation(self):
        project = Project.objects.create(
            title="My Project",
            description="A cool project",
        )
        self.assertEqual(project.title, "My Project")
        self.assertFalse(project.published)
        self.assertFalse(project.is_featured)

    def test_max_featured_projects(self):
        for i in range(3):
            Project.objects.create(
                title=f"Featured {i}",
                description="Desc",
                is_featured=True,
            )
        with self.assertRaises(ValueError):
            Project.objects.create(
                title="One Too Many",
                description="Desc",
                is_featured=True,
            )

    def test_featured_project_replace(self):
        projects = []
        for i in range(3):
            projects.append(Project.objects.create(
                title=f"Featured {i}",
                description="Desc",
                is_featured=True,
            ))
        projects[0].is_featured = False
        projects[0].save()
        Project.objects.create(
            title="New Featured",
            description="Desc",
            is_featured=True,
        )
        self.assertEqual(
            Project.objects.filter(is_featured=True).count(), 3
        )
