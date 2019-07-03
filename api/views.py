from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
import urllib3
from datetime import datetime, date, time
http = urllib3.PoolManager()
from api.models import Booking
from django.utils import timezone
import pytz

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
def booking(request, booking_id):
    # GET information about the status of a device.  Some way of securing this so only the app can 
    # access it will eventually be needed
    if request.method == 'GET': 
        try:
            booking = Booking.objects.get(pk=booking_id)
            return JsonResponse(booking.toJSON())
        except Booking.DoesNotExist:
            return JsonResponse({}, status=404)
        # if(booking):
        #     return JsonResponse(booking.toJSON())
        # else:
        #     return JsonResponse({}, status=404)

    # Make request to turn on a device.  A function should respond back with a value from the arduino
    # indicating success and this can be passed back to app
    elif request.method == 'POST': 
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        StartTime = body.get('StartTime')
        EndTime = body.get('EndTime')
        IDUser = body.get('IDUser')
        
        if not StartTime:
            return JsonResponse({"REASON": "Invalid StartTime provided"}, status=400)
        elif not EndTime:
            return JsonResponse({"REASON": "Invalid EndTime provided"}, status=400)
        elif not IDUser:
            return JsonResponse({"REASON": "Invalid IDUser provided"}, status=400)
        else:
            # this is our "happy path", once everything checks out, we send call to turn on device
            # Add your code to turn on the device here and the respond back.
            booking = Booking(IDUser=IDUser,StartTime=StartTime,EndTime=EndTime)
            resp = booking.save()
            print(resp)
            return JsonResponse(booking.toJSON())

@csrf_exempt 
def device(request, device_id):
    # GET information about the status of a device.  Some way of securing this so only the app can 
    # access it will eventually be needed
    if request.method == 'GET': 
        all_entries = Booking.objects.filter(IDUser="8305a3b2-72f4-4d5c-bd23-c7a0e746e183")
        print(all_entries)
        if(device_id == 1234):
            return JsonResponse({ "STATUS": "available", "booking": booking.toJSON()})
        else:
            return JsonResponse({}, status=404)

    # Make request to turn on a device.  A function should respond back with a value from the arduino
    # indicating success and this can be passed back to app
    elif request.method == 'POST': 
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        function_name = body.get('function_name')
        access_token = body.get('access_token')
        arg = body.get('arg')
        
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
                'arg':arg,
            } 
            endpoint = '%s/devices/%s/%s' % (API_ENDPOINT, device_id, function_name)
            r = http.request_encode_body('POST', endpoint, fields=post_data, encode_multipart=False)
            particle_response_data = json.loads(r.data.decode('utf-8'))
            if(r.status == 200):
                return JsonResponse({ "device" : { "UUID": device_id, "STATUS": "pending", "details": particle_response_data}})
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
