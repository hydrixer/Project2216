from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from iorder.models import drink
from iorder.serializers import Drinkserializer

@api_view(['GET','POST'])
def drink_list(request, format=None):
    if request.method=='GET':
        drinks = drink.objects.all()
        serializer = Drinkserializer(drinks,many=True)
        return Response(serializer.data)
    else:
        serializer = Drinkserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("eiwhjr")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def drink_detail(request,id, format=None):
    try:
        drk=drink.objects.get(pk=id)
    except drk.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer = Drinkserializer(drk)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer =Drinkserializer(drk,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        drk.delete()

# Create your views here.
