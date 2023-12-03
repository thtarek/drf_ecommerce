from django.contrib import admin
from django.urls import path
from .views import *


app_name = 'products'
urlpatterns = [
    # path('user-register/', user_registration_view, name='user_registration'),
    path('categories/', CategoryAPIView.as_view(), name='category-list'),
    path('create-product/', CreateProductAPIView.as_view(), name='create_product'),
<<<<<<< HEAD
    path('update-product/<int:pk>/', CreateProductAPIView.as_view(), name='update_product'),

=======
    path('product-list/', GetProductListAPIView.as_view(), name='product_list'),
>>>>>>> a3dc38e7e60d49cd7034a2e7c00ac3bc04b3d368

    
]