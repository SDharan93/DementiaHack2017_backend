from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import models
from . import serializers


class ListInstructions(APIView):
    def get(self, request, format=None):
        instructions = models.Instructions.objects.all()
        serializer = serializers.InstructionSerializer(instructions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.InstructionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

# TODO: Finish this endpoint
class DetailIntstructions(APIView):
    def get(self, request, format=None):
        instructions = models.Instructions.objects.all()
        serializer = serializers.InstructionSerializer(instructions, many=True)
        return Response(serializer.data)
