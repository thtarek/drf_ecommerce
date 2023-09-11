from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ["email","first_name","last_name", "is_admin","user_type"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password","first_name","last_name","user_type"]}),
        ("Permissions", {"fields": ["is_admin","email_verified"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(UserType)
admin.site.register(AddressUs)
