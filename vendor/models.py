import uuid
from django.db import models
from django.utils.text import slugify
from accounts.models import User, AddressUs


# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100, null=True, blank=True)
    business_username = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license', null=True,blank=True)
    nid_passport=models.ImageField(upload_to="media/nid_passport",blank=True,null=True)
    about_us = models.TextField(null=True, blank=True)
    followers=models.ManyToManyField(User,related_name="followers",blank=True)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)
    business_logo = models.ImageField(upload_to='media/business_logo/', null=True, blank=True)
    business_banner = models.ImageField(upload_to='media/business_banner/', null=True, blank=True)
    country_manager=models.ForeignKey(User, related_name="country_manager", on_delete=models.SET_NULL, null=True,blank=True)
    business_address = models.OneToOneField('accounts.AddressUS', on_delete=models.SET_NULL, null=True, blank=True)
    is_admin_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name
    def generate_uuid_slug(self):
        return str(uuid.uuid4().hex)

    def save(self, *args, **kwargs):
        if not self.vendor_slug:
            uuid_slug = self.generate_uuid_slug()
            base_slug = slugify(self.business_name)
            self.vendor_slug = f"{base_slug}-{uuid_slug}"
        super(Vendor, self).save(*args, **kwargs)
