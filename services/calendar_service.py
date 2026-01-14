import logging
from datetime import timedelta
from icalendar import Calendar, Event as CalEvent
from django.utils.timezone import now

logger = logging.getLogger(__name__)


class CalendarService:
    """
    Service for generating calendar event files (.ics) that can be imported
    into Google Calendar, Outlook, Apple Calendar, etc.
    """

    def generate_event_ics(self, event) -> bytes:
        """
        Generate an iCalendar (.ics) file for an event

        Args:
            event: Event model instance

        Returns:
            bytes: The .ics file content
        """
        cal = Calendar()
        cal.add('prodid', '-//Django Cameroon Events//djangocameroon.org//')
        cal.add('version', '2.0')
        cal.add('method', 'PUBLISH')

        cal_event = CalEvent()

        # Required fields
        cal_event.add('summary', event.title)
        cal_event.add('dtstart', event.date)

        # End time (default to 2 hours after start)
        end_time = event.date + timedelta(hours=2)
        cal_event.add('dtend', end_time)

        # Optional fields
        cal_event.add('dtstamp', now())
        cal_event.add('uid', f'event-{event.id}@djangocameroon.org')

        if event.description:
            cal_event.add('description', event.description)

        # Location
        if event.location:
            location_str = f"{event.location.name}, {event.location.city.name}"
            if hasattr(event.location.city, 'region'):
                location_str += f", {event.location.city.region.name}"
            cal_event.add('location', location_str)

        # Categories/Tags
        if event.tags.exists():
            categories = [tag.name for tag in event.tags.all()]
            cal_event.add('categories', categories)

        # Event type in description
        event_details = f"Type: {event.type}\n"
        if event.speakers.exists():
            speakers = ", ".join([speaker.name for speaker in event.speakers.all()])
            event_details += f"Speakers: {speakers}\n"

        existing_description = cal_event.get('description', '')
        if existing_description:
            cal_event['description'] = f"{existing_description}\n\n{event_details}"
        else:
            cal_event.add('description', event_details)

        # Status
        cal_event.add('status', 'CONFIRMED' if event.published else 'TENTATIVE')

        # Add event to calendar
        cal.add_component(cal_event)

        return cal.to_ical()

    def generate_filename(self, event) -> str:
        """
        Generate a filename for the .ics file

        Args:
            event: Event model instance

        Returns:
            str: Filename for the .ics file
        """
        # Clean the title to make it filesystem-safe
        safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in event.title)
        safe_title = safe_title.replace(' ', '_').lower()
        return f"{safe_title}.ics"
