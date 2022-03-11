#Django
from django.db import models
from django.contrib.auth.models import AbstractUser


class Client(AbstractUser):

    """Users within the Django authentication system are represented by this
    model.
    Email and password are required. Other fields are optional."""
    
    first_name =    models.CharField(max_length=150, blank=True)
    last_name =     models.CharField(max_length=150, blank=True)
    email =         models.EmailField(unique=True, blank=True)
    document =      models.CharField(max_length=10)
    is_staff =      models.BooleanField(default=False)
    is_active =     models.BooleanField(default=True)
    
    is_verified =   models.BooleanField(
        "verified",
        default=False,
        help_text="Set to true when the user have verified its email address. "
    )

    USERNAME_FIELD =    'email'
    REQUIRED_FIELDS =   ['username', 'first_name', 'last_name', 'document']

    def __str__(self):
        """Return First name"""
        return self.first_name