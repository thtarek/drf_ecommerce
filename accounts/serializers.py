from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import *


class AddressUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressUs
        fields = ['user','phone_number', 'address_one', 'address_two', 'city', 'zipcode', 'country']

    def validate_phone_number(self, value):
        # Implement your custom phone number validation logic here
        if not value.isdigit() or len(value) < 11:
            raise serializers.ValidationError("Invalid phone number.")
        elif AddressUs.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number already exists.")
        return value

class UserRegistrationSerializer(serializers.ModelSerializer):
    user_address = AddressUsSerializer(many=True)
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name','avatar','user_type', 'gender', 'user_address']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address already exists.")
        return value
    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError("First name is required.")
        return value

    def validate_last_name(self, value):
        if not value:
            raise serializers.ValidationError("Last name is required.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        addresses = validated_data.pop('user_address')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        for address in addresses:
            AddressUs.objects.create(user=user, **address)
        return user
    
class CreateUserTypeSerializer(serializers.ModelSerializer):
    key = serializers.CharField()
    class Meta:
        model = UserType
        fields = ["id","key","value"]
    
    def validate_value(self, value):
        if len(value) > 11:
            raise ValidationError("Length of value less then or equal 10")
        return value
    def validate_key(self, value):
        if UserType.objects.filter(key=value).exists():
            raise serializers.ValidationError("The key must be unique.")
        return value
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['email','password']
  