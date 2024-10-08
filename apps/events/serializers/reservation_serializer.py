from rest_framework import serializers

from apps.events.models.reservation import Reservation
from apps.users.serializers.general_serializers import UserMinSerializer


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = UserMinSerializer(instance.user).data
        return representation


class CreateReservationInputSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a reservation.
    This serializer is used to validate the input data.
    """

    class Meta:
        model = Reservation
        exclude = ("check_in", "user")


class CreateReservationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a reservation.
    This serializer is used to create the reservation.
    """

    class Meta:
        model = Reservation
        exclude = ("check_in",)

    def validate(self, data):
        # Check if the user has already made a reservation for the event
        if Reservation.objects.filter(
                for_event=data["for_event"], user=data["user"]
        ).exists():
            raise serializers.ValidationError(
                "You have already made a reservation for this event."
            )
        return data
