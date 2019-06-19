from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse


def index(request):
    if request.method == 'GET': 
        return JsonResponse({ "message": "I will process a get"})
    elif request.method == 'POST': 
        return JsonResponse({ "message": "I will process a post"})