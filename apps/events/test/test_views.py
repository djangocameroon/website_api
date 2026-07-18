from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now, timedelta

from apps.events.models.event import Event, EventCity, EventRegion, EventVenue


class EventUpcomingFilterTest(TestCase):
    def setUp(self):
        region = EventRegion.objects.create(name="Centre")
        city = EventCity.objects.create(name="Yaounde", region=region)
        venue = EventVenue.objects.create(name="Hub", city=city)

        self.past_event = Event.objects.create(
            title="Past Meetup",
            description="Already happened",
            location=venue,
            date=now() - timedelta(days=3),
            type="Online",
            category="Talks",
            published=True,
        )
        self.unpublished_event = Event.objects.create(
            title="Draft Meetup",
            description="Not published yet",
            location=venue,
            date=now() + timedelta(days=2),
            type="Online",
            category="Talks",
            published=False,
        )
        self.soon_event = Event.objects.create(
            title="Soon Meetup",
            description="Happening soon",
            location=venue,
            date=now() + timedelta(days=1),
            type="Online",
            category="Talks",
            published=True,
        )
        self.later_event = Event.objects.create(
            title="Later Meetup",
            description="Happening later",
            location=venue,
            date=now() + timedelta(days=10),
            type="Online",
            category="Talks",
            published=True,
        )

    def test_upcoming_filter_excludes_past_and_unpublished_and_orders_by_date(self):
        response = self.client.get(reverse("events-list"), {"upcoming": "true"})
        self.assertEqual(response.status_code, 200)
        titles = [event["title"] for event in response.json()["data"]]
        self.assertEqual(titles, ["Soon Meetup", "Later Meetup"])

    def test_without_upcoming_filter_returns_all_events(self):
        response = self.client.get(reverse("events-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 4)
