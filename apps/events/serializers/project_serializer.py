from rest_framework import serializers
from apps.events.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'tags',
            'github_link',
            'demo_link',
            'thumbnail',
            'is_featured',
            'created_at'
        ]
