from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse


def index(request, id=1234):
    if request.method == 'GET': 
        return JsonResponse({ "METHOD": request.method, "id": id})
    elif request.method == 'POST': 
        print(request.body)
        return JsonResponse({ "message": "I will process a post"})