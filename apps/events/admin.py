import os
from django import forms
from django.contrib import admin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpRequest
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.widgets import UnfoldAdminFileFieldWidget, UnfoldAdminTextInputWidget

from apps.events.models import (
    Event, EventCity, EventRegion,
    EventVenue, EventTag, Reservation,
    Speaker, SpeakerSocialMedia, SpeakerSpeciality,
)
from apps.events.models.constants import SOCIAL_MEDIA_PLATFORMS


@admin.register(EventRegion)
class EventRegionAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    def has_module_permission(self, request: HttpRequest) -> bool:
        return False # Hide the EventRegion model from the admin index page


@admin.register(EventCity)
class EventCityAdmin(ModelAdmin):
    list_display = ("name", "region")
    list_filter = ("region",)
    search_fields = ("name", "region__name")
    autocomplete_fields = ("region",)
    ordering = ("region__name", "name")
    
    def has_module_permission(self, request: HttpRequest) -> bool:
        return False # Hide the EventCity model from the admin index page


@admin.register(EventVenue)
class EventVenueAdmin(ModelAdmin):
    list_display = ("name", "city", "region_name")
    list_filter = ("city__region", "city")
    search_fields = ("name", "city__name", "city__region__name")
    autocomplete_fields = ("city",)
    ordering = ("city__region__name", "city__name", "name")

    @admin.display(description="Region")
    def region_name(self, obj):
        return obj.city.region.name
    
    def has_module_permission(self, request: HttpRequest) -> bool:
        return False # Hide the EventVenue model from the admin index page


@admin.register(SpeakerSpeciality)
class SpeakerSpecialityAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    def has_module_permission(self, request):
        return False

class SpeakerSocialMediaInline(TabularInline):
    model = SpeakerSocialMedia
    extra = 1
    fields = ("platform", "profile_link", "active")

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        used_platforms = set(
            obj.social_media.values_list("platform", flat=True)
        ) if obj else set()

        class PlatformChoiceForm(formset.form):
            def __init__(self, *args, **kw):
                super().__init__(*args, **kw)
                current = self.instance.platform if self.instance.pk else None
                self.fields["platform"].choices = [
                    choice for choice in SOCIAL_MEDIA_PLATFORMS
                    if choice[0] not in used_platforms or choice[0] == current
                ]

        formset.form = PlatformChoiceForm
        return formset


class SpeakerForm(forms.ModelForm):
    photo = forms.CharField(
        required=False,
        widget=UnfoldAdminTextInputWidget,
        help_text="Photo URL, or upload a file below instead.",
    )
    photo_file = forms.FileField(
        required=False,
        widget=UnfoldAdminFileFieldWidget,
        help_text="Upload a photo file (overrides the URL above).",
    )

    class Meta:
        model = Speaker
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        photo_file = cleaned_data.get("photo_file")
        if photo_file:
            file_name = default_storage.save(photo_file.name, ContentFile(photo_file.read()))
            cleaned_data["photo"] = default_storage.url(file_name)
            if os.getenv("ENVIRONMENT") == "development":
                cleaned_data["photo"] = f"http://localhost:8912{cleaned_data['photo']}"
                
        return cleaned_data


@admin.register(Speaker)
class SpeakerAdmin(ModelAdmin):
    form = SpeakerForm
    list_display = ("name", "speciality", "active", "photo_preview")
    list_filter = ("active", "speciality")
    search_fields = ("name", "bio")
    autocomplete_fields = ("speciality",)
    readonly_fields = ("slug", "photo_preview")
    inlines = [SpeakerSocialMediaInline]
    ordering = ("name",)

    @admin.display(description="Photo")
    def photo_preview(self, obj):
        if not obj.photo:
            return "-"
        return format_html(
            '<img src="{}" style="height:48px;width:48px;border-radius:50%;object-fit:cover;" />',
            obj.photo,
        )


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ("title", "category", "type", "for_community", "date", "published", "location")
    list_filter = ("published", "category", "type", "for_community", "date")
    search_fields = ("title", "description", "slug")
    autocomplete_fields = ("location",)
    filter_horizontal = ("speakers", "tags")
    readonly_fields = ("slug", "created_at", "updated_at", "created_by", "updated_by")
    date_hierarchy = "date"
    ordering = ("-date",)
    fieldsets = (
        (None, {"fields": ("title", "slug", "description", "thumbnail")}),
        ("Classification", {"fields": ("category", "type", "for_community", "published")}),
        ("Location & Date", {"fields": ("location", "date")}),
        ("Speakers & Tags", {"fields": ("speakers", "tags")}),
        ("Metadata", {"fields": ("created_by", "updated_by", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

@admin.register(EventTag)
class EventTagAdmin(ModelAdmin):
    def has_module_permission(self, request):
        return False

admin.site.register(Reservation)
