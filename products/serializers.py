from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import *

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
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CreateProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    color = serializers.PrimaryKeyRelatedField(many=True, queryset=Color.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    size = serializers.PrimaryKeyRelatedField(many=True, queryset=ProductSize.objects.all())
    unit = serializers.PrimaryKeyRelatedField(queryset=ProductUnit.objects.all(), allow_null=True)
    delivery_countries = serializers.PrimaryKeyRelatedField(many=True, queryset=Country.objects.all())

    
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
        product = Product.objects.create(**validated_data)
        product.color.set(color_data)
        product.size.set(size_data)
        product.delivery_countries.set(delivery_countries_data)
        return product