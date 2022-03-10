#Django
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password


# class CustomClientManager(BaseUserManager):
#     """ Manage creation of users """

#     def create_user(self, email, first_name, last_name, password, document, **other_fields):
#         """ Create a new regular client """
#         email = self.normalize_email(email=email)
#         client = self.model(email=email, first_name=first_name, last_name=last_name, document=document,**other_fields)
#         client.make_password(password)
#         client.save()
#         return client
    
#     def create_superuser(self, email, first_name, last_name, password, document, **other_fields):
#         """ Create an admin user """
#         other_fields.setdefault("is_staff", True)
#         other_fields.setdefault('is_superuser',True)
#         other_fields.setdefault('is_active',True)

#         if other_fields.get('is_staff') is not True:
#             raise ValueError(
#                 'Superuser must be assigned to is_staff = True')
#         if other_fields.get('is_superuser') is not True:
#             raise ValueError(
#                 'Superuser must be assigned to is_staff = True')

#         return self.create_user(email=email, first_name=first_name,last_name=last_name,password=password, document=document,**other_fields)
            

class Client(AbstractUser):
    """Users within the Django authentication system are represented by this
    model.
    Email and password are required. Other fields are optional."""
    
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True, blank=True)
    document = models.CharField(max_length=10)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    is_verified = models.BooleanField(
        "verified",
        default=True,
        help_text="Set to true when the user have verified its email address. "
    )

    #EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'document']
    
    #objects = CustomClientManager()

    def __str__(self):
        """Return First name"""
        
        return self.first_name