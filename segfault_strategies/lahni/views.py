from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import apiai
import json
import os

from . import models
from . import serializers


def getChatBotResponse(query):
    #ai = apiai.ApiAI(os.environ['API_AI_TOKEN'])
    ai = apiai.ApiAI("67b421850fed43b3abf8de1abaa5b8b0")
    request = ai.text_request()
    request.lang = 'en'  # optional, default value equal 'en'
    request.session_id = "98712368890037229297654random_key"  # This should be randomly generated...
    request.query = query
    response = request.getresponse()
    responsestr = response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    return response_obj


class ListInstructions(APIView):
    def get(self, request, format=None):
        instructions = models.Instructions.objects.all()
        serializer = serializers.InstructionSerializer(instructions, many=True)

        return Response({'something': 'something'})

    def post(self, request, format=None):

        if 'query' in request.data:
            # Do api ai logic
            query = request.data['query']
            apiResponse = getChatBotResponse(query)

            # lets assume the api response is not changing...
            intentID = None
            author = "Generated"
            actionIncomplete = True
            message = None

            if 'result' in apiResponse:
                if 'metadata' in apiResponse['result']:
                    if 'intentId' in apiResponse['result']['metadata']:
                        intentID = apiResponse['result']['metadata']['intentId']

            if 'result' in apiResponse:
                if 'actionIncomplete' in apiResponse['result']:
                    actionIncomplete = apiResponse['result']['actionIncomplete']

            if 'result' in apiResponse:
                if 'fulfillment' in apiResponse['result']:
                    if 'messages' in apiResponse['result']['fulfillment']:
                        message = apiResponse['result']['fulfillment']['messages'][0]['speech']

            question = models.Instructions.objects.get(intentID=intentID)
            if not question:
                question = models.Instructions(intentID, author)

            response = {}
            response['intentID'] = intentID
            response['actionIncomplete'] = actionIncomplete
            response['message'] = message
            return Response(response, status=status.HTTP_200_OK)

        else:
            return Response('Please send a query. Example: How do I make coffee?', status=status.HTTP_400_BAD_REQUEST)

# TODO: Finish this endpoint
class DetailIntstructions(APIView):
    def get(self, request, format=None):
        instructions = models.Instructions.objects.all()
        serializer = serializers.InstructionSerializer(instructions, many=True)
        return Response(serializer.data)
