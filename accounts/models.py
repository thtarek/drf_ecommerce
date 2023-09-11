from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserType(models.Model):
    key = models.CharField(max_length=255, null=True, blank=True, unique=True)
    value = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return "[%s]: %s" % (self.id, self.key)

class AddressUs(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_address', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address_one = models.CharField(max_length=300, null=True, blank=True)
    address_two = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=2, null=True, blank=True)


    def __str__(self):
        return self.user.first_name
    



class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name,last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        blank=True,  
        null=True,
    )
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('3RD_GENDER', 'Third Gender'),
    )
    first_name = models.CharField(max_length=50,blank=True, null=True)
    last_name = models.CharField(max_length=50,blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, db_column='user_type', blank=True, null=True, related_name="usertype")
    gender = models.CharField(choices=GENDER_CHOICE,max_length=12, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    


   

  