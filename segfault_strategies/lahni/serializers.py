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

    def create(self, validated_data):
        return models.Instructions(**validated_data)


class StepSerializer(serializers.Serializer):
    class Meta:
        field = (
            'title',
            'message',
            'failureCount'
        )
        model = models.Steps

    def create(self, validated_data):
        return models.Steps(**validated_data)

class MediaSerializer(serializers.Serializer):
    class Meta:
        field = (
            'audio',
            'video',
            'picture'
        )
        model = models.Media

    def create(self, validated_data):
        return models.Media(**validated_data)
