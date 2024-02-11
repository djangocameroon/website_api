from rest_framework import serializers

from apps.events.models.reservation import Reservation


class ReservationInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            "event",
            "email",
            "full_name",
            "sex",
        )


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
