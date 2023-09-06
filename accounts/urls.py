from django.contrib import admin
from django.urls import path
from .views import user_registration_view


app_name = 'accounts'
urlpatterns = [
    path('register/', user_registration_view, name='user-registration'),
]