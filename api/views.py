from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
import urllib3
http = urllib3.PoolManager()
API_ENDPOINT = "https://api.particle.io/v1"

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
def device(request, device_id):
    # GET information about the status of a device.  Some way of securing this so only the app can 
    # access it will eventually be needed
    if request.method == 'GET': 
        if(id == 1234):
            return JsonResponse({ "STATUS": "available"})
        else:
            return JsonResponse({}, status=404)

    # Make request to turn on a device.  A function should respond back with a value from the arduino
    # indicating success and this can be passed back to app
    elif request.method == 'POST': 
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        function_name = body.get('function_name')
        access_token = body.get('access_token')
        
        if not function_name:
            return JsonResponse({"REASON": "Invalid action provided"}, status=400)
        elif not access_token:
            return JsonResponse({"REASON": "Invalid user token provided"}, status=400)
        elif not device_id:
            return JsonResponse({"REASON": "Invalid device ID provided"}, status=400)
        else:
            # this is our "happy path", once everything checks out, we send call to turn on device
            # Add your code to turn on the device here and the respond back.
            post_data = {
                'access_token':access_token,
                'arg':0,
            } 
            endpoint = '%s/devices/%s/%s' % (API_ENDPOINT, device_id, function_name)
            r = http.request('POST', endpoint, fields=post_data)
            particle_response_data = json.loads(r.data.decode('utf-8'))
            if(r.status == 200):
                return JsonResponse({ "device" : { "UUID": id, "STATUS": "pending", "details": particle_response_data}})
            else:
                return JsonResponse({ "STATUS" : "error", "code": r.status, "details": particle_response_data})

# A basic example of how some other requests might be structured.  This will only respond to GET
@csrf_exempt 
def listDevices(request):
    if request.method == 'GET': 
        access_token = request.GET.get('access_token')
        r = http.request('GET', '%s/devices?access_token=%s' % (API_ENDPOINT, access_token))
        particle_response_data = json.loads(r.data.decode('utf-8'))
        return JsonResponse({"devices": particle_response_data})
    else:
        return JsonResponse({}, status=405)
