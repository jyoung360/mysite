from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid

@csrf_exempt 
def login(request):
    # Login request.  App sends credentials and gets back a TOKEN to store for future requests
    # Only POST allowed, never accept sensitive information over a GET request
    if request.method == 'POST': 
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body.get('username')
        password = body.get('password')
        return JsonResponse({ "STATUS": "success", "TOKEN": uuid.uuid4()})

@csrf_exempt 
def device(request, id):
    # GET information about the status of a device.  Some way of securing this so only the app can 
    # access it will eventually be needed
    if request.method == 'GET': 
        if(id == 1234):
            return JsonResponse({ "STATUS": "available"})
        else:
            return JsonResponse({}, status=404)

    # Make request to turn on a device.  This request will always return to the app with a success,
    # the arduino will take time to actually turn on the relay and respond back, and you shouldn't 
    # block waiting for that to happen.  "pending" is a reasonable state to use
    elif request.method == 'POST': 
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        action = body.get('action')
        token = body.get('token')
        
        if not action:
            return JsonResponse({"REASON": "Invalid action provided"}, status=400)
        elif not token:
            return JsonResponse({"REASON": "Invalid user token provided"}, status=400)
        elif id != 1234:
            return JsonResponse({"REASON": "Invalid device ID provided"}, status=400)
        else:
            # this is our "happy path", once everything checks out, we send call to turn on device
            # Add your code to turn on the device here and the respond back.
            return JsonResponse({ "device" : { "UUID": id, "STATUS": "pending"}})

# A basic example of how some other requests might be structured.  This will only respond to GET
@csrf_exempt 
def listDevices(request):
    if request.method == 'GET': 
        return JsonResponse({"devices": [uuid.uuid4(),uuid.uuid4(),uuid.uuid4()]})
    else:
        return JsonResponse({}, status=405)