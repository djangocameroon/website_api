from rest_framework import serializers

from apps.events.models.reservation import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
        read_only_fields = ("id", "created_at", "check_in")
