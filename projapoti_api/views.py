from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import service
# Create your views here.

@api_view(['GET'])
def getAllUser(request):
    response=service.getAllUser()
    return Response(response)

@api_view(['POST'])
def registration(request):
    response=service.registration(request.data)
    return Response(response)

@api_view(['POST'])
def login(request):
    email=request.data.get("Email")
    password=request.data.get("Password")
    response=service.login(email,password)
    return Response(response)

@api_view(['POST'])
def varify_token(request):
    email=request.data.get("Email")
    password=request.data.get("Password")
    token=request.data.get("Token")
    response=service.varify_token(token,email,password)
    return Response(response)

