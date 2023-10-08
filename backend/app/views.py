from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

def index(request):
    # return HttpResponse("Welcome")
    d = {
        'name': 'junj',
        'age': 20,
        'sex': 'male'
    }
    return JsonResponse(d)

