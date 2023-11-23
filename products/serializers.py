from rest_framework import serializers
from django.db import transaction
from django.core.exceptions import ValidationError
from helpers.image import base64_to_image
from .models import *
from accounts.models import *



class UserSerializerForProductList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_category']

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
class BrandSerializerForGetProduct(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id','name']
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
class ProductFeaturedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeaturedImage
        fields = '__all__'
class ProductGalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGalleryImage
        fields = '__all__'
class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetails
        fields = '__all__'
        extra_kwargs = {
            'product': {'required': False},
            'description': {'required': False, 'allow_blank': True},
            'specification': {'required': False, 'allow_blank': True},
        } 
class GetProductSerializer(serializers.ModelSerializer):
    vendor = UserSerializerForProductList()
    featured_image = ProductFeaturedImageSerializer(read_only=True)
    brand = BrandSerializerForGetProduct()
    class Meta:
        model = Product
        exclude = ('unit','cost_price','status','is_delete','created_at','updated_at' )
        depth=1
        
class CreateProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    color = serializers.PrimaryKeyRelatedField(many=True, queryset=Color.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    size = serializers.PrimaryKeyRelatedField(many=True, queryset=ProductSize.objects.all())
    unit = serializers.PrimaryKeyRelatedField(queryset=ProductUnit.objects.all(), allow_null=True)
    delivery_countries = serializers.PrimaryKeyRelatedField(many=True, queryset=Country.objects.all())
    featured_image = serializers.CharField()
    gallery_images = serializers.ListField(child=serializers.CharField(), write_only=True)
    product_details = ProductDetailsSerializer(write_only=True)

    class Meta:
        model = Product
        fields = '__all__'
    def validate(self, data):

        # Validate name
        name = data.get('name')
        if not name:
            raise serializers.ValidationError("Name is required.")

        # Validate brand
        brand = data.get('brand')
        if not brand:
            raise serializers.ValidationError("Brand is required.")

        # Validate cost_price
        cost_price = data.get('cost_price')
        if cost_price is None or cost_price < 0:
            raise serializers.ValidationError("Cost price is required and cannot be negative.")

        # Validate regular_price
        regular_price = data.get('regular_price')
        if regular_price is None or regular_price < 0:
            raise serializers.ValidationError("Regular price is required and cannot be negative.")

        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user 
        validated_data['vendor'] = user
        color_data = validated_data.pop('color', [])
        size_data = validated_data.pop('size', [])
        delivery_countries_data = validated_data.pop('delivery_countries', [])
        gallery_images_data = validated_data.pop('gallery_images', [])
        featured_image = validated_data.pop('featured_image')
        quantity = validated_data.get('quantity_in_stock')
        product_details_data = validated_data.pop('product_details',{})
        
        with transaction.atomic():
            product = Product.objects.create(**validated_data)
            product.color.set(color_data)
            product.size.set(size_data)
            product.delivery_countries.set(delivery_countries_data)
            """
                for featured image and gallery image. Hare save only one singale featured_image and multiple gallery_images. 
            """
            file_path_195x192 = base64_to_image(featured_image, re_size=(195, 192))
            ProductFeaturedImage.objects.create(product=product, image_195_X_192=file_path_195x192)
            for img in gallery_images_data:
                file_path_195x192 = base64_to_image(img, re_size=(195, 192))
                file_path_270x180 = base64_to_image(img, re_size=(270, 180))
                ProductGalleryImage.objects.create(product=product, image_195_X_192=file_path_195x192, image_270_X_180=file_path_270x180)
            productInventory.objects.create(product=product, quantity=quantity)
            description = product_details_data.get('description')
            specification = product_details_data.get('specification')
            product_details = ProductDetails.objects.filter(product=product).first()

            if not product_details:
                product_details = ProductDetails.objects.create(product=product, description=description, specification=specification)
           
        return product