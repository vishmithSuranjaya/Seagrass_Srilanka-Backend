from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager

def user_image_upload_path(instance, filename):
    return f'user/{filename}'


class Users(AbstractBaseUser, PermissionsMixin):
    # user model for JWT authentication 

    user_id = models.CharField(max_length=10, unique= True, primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length =50)
    email = models.EmailField(max_length=70, unique=True)
    blog_id = models.CharField(max_length=10, blank=True, null = True)
    cart_id = models.CharField(max_length=15, blank = True, null = True )
    comment_id = models.CharField(max_length =20, blank = True, null =True )
    image = models.ImageField(upload_to=user_image_upload_path, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default = False)
    date_joined = models.DateTimeField(default = timezone.now)
    last_login = models.DateTimeField(null = True, blank = True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname']

    def __str__(self):
        return f"{self.fname} {self.lname} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.fname} {self.lname}"
    

# Create your models here.
