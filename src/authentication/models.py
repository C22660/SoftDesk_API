from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Users(AbstractUser):
    """stocke les identifiants de connexion des utilisateurs"""
    # user_id(IntegerField)
    # first_name(CharField)
    first_name = models.CharField(max_length=15, verbose_name="prenom")
    # last_name(CharField)
    last_name = models.CharField(max_length=15, verbose_name="nom")
    # email(EmailField)
    email = models.EmailField(unique=True, max_length=255, blank=False)
    # password(CharField)
    # non redéfinit




    # ------ A intégrer ici au lieu de rôle dans contributors ? -------
    # AUTHOR = 'AUTHOR'
    # CONTRIBUTOR = 'CONTRIBUTOR'
    #
    # ROLE_CHOICES = (
    #     (AUTHOR, 'Auteur'),
    #     (CONTRIBUTOR, 'Contributeur'),
    # )
    #
    # role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')