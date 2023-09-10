from django.contrib import admin
from django.urls import path
from .views import *


app_name = 'accounts'
urlpatterns = [
    path('register/', user_registration_view, name='user-registration'),
    path('create-user-type/', create_user_type_view, name='create_user_type'),
]