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
    ai = apiai.ApiAI("546ff8d340c849c4b2236e1294920209")
    request = ai.text_request()
    request.lang = 'en'  # optional, default value equal 'en'
    request.session_id = "93782788623872010981276898798192813"  # This should be randomly generated...
    request.query = query
    request.resetContexts = False
    response = request.getresponse()
    responsestr = response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    return response_obj


class ListInstructions(APIView):
    def get(self, request, format=None):
        # Very hacky way to paginate
        pagination_size = 10
        instructions = models.Instructions.objects.filter(isComplete=False).order_by('-createdAt')[:pagination_size]

        response = {'instructions': []}
        for instruction in instructions:
            item = {'internalID': instruction.intentID, 'createdAt': instruction.createdAt}
            response['instructions'].append(item)

        return Response(response, status.HTTP_200_OK)

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
            payload = None

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
                        last_element = len(apiResponse['result']['fulfillment']['messages']) - 1
                        if 'payload' in apiResponse['result']['fulfillment']['messages'][last_element]:
                            payload = apiResponse['result']['fulfillment']['messages'][last_element]['payload']
                            message = ""
                        elif 'speech' in apiResponse['result']['fulfillment']['messages'][last_element]:
                            message = apiResponse['result']['fulfillment']['messages'][last_element]['speech']
                        else:
                            return Response({'err': 'could not get a response'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            completion_status = not actionIncomplete
            question = models.Instructions.objects.filter(intentID=intentID)
            if not question:
                question = models.Instructions.objects.create(intentID=intentID, author=author, isComplete=completion_status)
            else:
                question.update(isComplete=completion_status)

            response = {}
            response['intentID'] = intentID
            response['actionIncomplete'] = actionIncomplete
            if payload:
                response['steps'] = payload['Instructions']
            elif message:
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
