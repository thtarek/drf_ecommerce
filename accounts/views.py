from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

# Create your views here.

@api_view(['POST'])
def user_registration_view(request):
    if request.method == "POST":
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            response_data = {
                "message": "User registered successfully",
                "user_id": user.id,
                "email": user.email,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def create_user_type_view(request):
    if request.method == "GET":
        queryset = UserType.objects.all()
        if not queryset:
            return Response({"message": "No user types found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CreateUserTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = CreateUserTypeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # tt = serializer.validated_data['key']
            type = serializer.save()
            response_data = {"message": "Create new user type successfully"}
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH','DELETE'])
def manage_user_type_view(request, pk):
    instance = get_object_or_404(UserType, id=pk)
    if request.method == 'PATCH':
        serializer = CreateUserTypeSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                "status":True,
                "message": "User type updated successfully.",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        instance.delete()
        return Response({"message": "User type deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    


