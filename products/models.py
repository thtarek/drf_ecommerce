from django.db import models

from accounts.models import User

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True, null=True, blank=True)  # Country code (e.g., "USA", "CAN")

    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True,)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Color(models.Model):
    name = models.CharField(max_length=100,  null=True, blank=True)
    hex_code = models.CharField(max_length=7, unique=True)  # Represented as a 7-character hexadecimal code (e.g., #RRGGBB)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True)

    def __str__(self):
        return self.name
class ProductSize(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name
class ProductUnit(models.Model):
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    vendor = models.ForeignKey(User ,on_delete=models.DO_NOTHING, related_name="vendor_products",null=True,blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=300, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="category_products")
    color = models.ManyToManyField(Color)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name="barand_products")
    size = models.ManyToManyField(ProductSize)
    unit = models.ForeignKey(ProductUnit, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)
    barcode = models.ImageField(upload_to='product_barcode_image/', null=True, blank=True)


    def __str__(self):
        return self.name
    
class ProductFeaturedImage(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='featured_image')
    image_195_X_192 = models.ImageField(upload_to='product_featured_images/')

    def __str__(self):
        return f"Featured Image for {self.product.name}"
    
class ProductGalleryImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image_195_X_192 = models.ImageField(upload_to='product_gallery_images/')
    image_270_X_180 = models.ImageField(upload_to='product_gallery_images/')

    def __str__(self):
        return f"Gallery Image for {self.product.name}"
    
class ProductDeliveryLocation(models.Model):

    charge = models.DecimalField(max_digits=10, decimal_places=2)     
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name