from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 'address', 'role', 'gender']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email already exists.")
        return value

    def validate_phone_number(self, value):
        # Implement your custom phone number validation logic here
        if not value.isdigit() or len(value) < 11:
            raise ValidationError("Invalid phone number.")
        return value

    def validate_first_name(self, value):
        if not value:
            raise ValidationError("First name is required.")
        return value

    def validate_last_name(self, value):
        if not value:
            raise ValidationError("Last name is required.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user