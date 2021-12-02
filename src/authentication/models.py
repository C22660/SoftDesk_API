from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Users(AbstractUser):
    """stocke les identifiants de connexion des utilisateurs"""
    first_name = models.CharField(max_length=15, verbose_name="prenom")
    last_name = models.CharField(max_length=15, verbose_name="nom")
    email = models.EmailField(unique=True, max_length=255, blank=False)
