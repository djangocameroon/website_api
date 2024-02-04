from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from apps.events.models.speaker import Speaker
from apps.events.serializers.speaker_serializer import SpeakerSerializer


class SpeakerViewSet(ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [AllowAny]
