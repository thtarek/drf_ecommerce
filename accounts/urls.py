from django.contrib import admin
from django.urls import path
from .views import *


app_name = 'accounts'
urlpatterns = [
    path('user-register/', user_registration_view, name='user_registration'),
    path('create-user-type/', create_user_type_view, name='create_user_type'),
    path('manage-user-type/<int:pk>/', manage_user_type_view, name='manage_user_type_view'),
]