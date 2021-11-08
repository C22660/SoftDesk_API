from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    AUTHOR = 'AUTHOR'
    CONTRIBUTOR = 'CONTRIBUTOR'

    ROLE_CHOICES = (
        (AUTHOR, 'Autheur'),
        (CONTRIBUTOR, 'Contributeur'),
    )

    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')