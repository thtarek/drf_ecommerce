from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

# Create your views here.

@api_view(['POST'])
def user_registration_view(request):
    if request.method == "POST":
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            response_data = {
                "message": "User registered successfully",
                "user_id": user.id,
                "email": user.email,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_user_type_view(request):
    if request.method == "POST":
        serializer = CreateUserTypeSerializer(data=request.data)
        if serializer.is_valid():
            # tt = serializer.validated_data['key']
            type = serializer.save()
            response_data = {"message": "Create new user type successfully"}
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


