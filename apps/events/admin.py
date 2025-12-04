from django.contrib import admin

from apps.events.models import (
    Event, EventCity, EventRegion,
    EventVenue, EventTag, Reservation,
    Speaker, SpeakerSocialMedia, SpeakerSpeciality,
    AvailableSocialMedia,
)

admin.site.register(Event)
admin.site.register(EventCity)
admin.site.register(EventRegion)
admin.site.register(EventVenue)
admin.site.register(EventTag)
admin.site.register(Reservation)
admin.site.register(Speaker)
admin.site.register(SpeakerSocialMedia)
admin.site.register(SpeakerSpeciality)
admin.site.register(AvailableSocialMedia)
