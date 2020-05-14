from django.db import models
from improved_user.model_mixins import AbstractUser

# Create your models here.
class User(AbstractUser):
    """A User model that extends the Improved User"""
    def __str__(self):
        return self.email
