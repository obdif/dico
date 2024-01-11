from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

class History(models.Model):
    word = models.CharField(max_length = 50)
    date_searched = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return self.word
    

# class UserAccount(models.Model):
#     email = models.EmailField(unique=True)
#     history = models.TextField(blank=True)
#     favorite_words = models.TextField(blank=True)

#     def __str__(self):
#         return self.email


    
    