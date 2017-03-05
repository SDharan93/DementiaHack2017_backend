from rest_framework import serializers

from . import models


class InstructionSerializer(serializers.Serializer):
    class Meta:
        fields = (
            'id',
            'author',
            'intentID',
            'createdAt'
        )
        model = models.Instructions


class StepSerializer(serializers.Serializer):
    class Meta:
        field = (
            'title',
            'message',
            'failureCount'
        )
        model = models.Steps

class MediaSerializer(serializers.Serializer):
    class Meta:
        field = (
            'audio',
            'video',
            'picture'
        )
        model = models.Media
