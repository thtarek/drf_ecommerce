from django.contrib import admin
from django.urls import path
from .views import *


app_name = 'products'
urlpatterns = [
    # path('user-register/', user_registration_view, name='user_registration'),
    path('categories/', CategoryAPIView.as_view(), name='category-list'),
    path('create-product/', CreateProductAPIView.as_view(), name='create_product'),

    
]