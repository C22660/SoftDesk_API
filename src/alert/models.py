# from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

# Create your models here.


# ou User de contrib.auth ?
# class Users(models.Model):
#     """stocke les identifiants de connexion des utilisateurs"""
#     # user_id(IntegerField)
#     # first_name(CharField)
#     first_name = models.CharField(max_length=15, verbose_name="prenom")
#     # last_name(CharField)
#     last_name = models.CharField(max_length=15, verbose_name="nom")
#     # email(EmailField)
#     email = models.EmailField(unique=True, max_length=255, blank=False)
#     # password(CharField)
#     password = models.CharField


PROJECT_CHOICES = (('Back-end', 'Back-end'), ('Front-end', 'Front-end'),
                   ('iOS', 'iOS'), ('Android', 'Android'))


class Projects(models.Model):
    """stocke toutes les informations concernant chaque projet/produit/application
     en cours de développement ou de gestion dans l'entreprise.
     Relation plusieurs-à-plusieurs avec la table des utilisateurs,
     via une table de jonction appelée Contributors"""
    # project_id(IntegerField)
    # title(Charfield)
    title = models.CharField(max_length=128, verbose_name="Titre")
    # description(CharField)
    description = models.CharField(max_length=200)
    # type(Charfield)
    type = models.CharField(max_length=30, choices=PROJECT_CHOICES)
    # relation un-à-plusieurs avec la table Users pour enregistrer l'auteur du projet
    # possibilité de gérer ce cas à l'aide du champ d'autorisation de la classe Contributor
    # author_user_id(ForeignKey)  => lien contributors
    # permetrtait de récupérer les contributions d'un utilisateur avec user.contributions en
    # ajoutant related_name="contributions" si contributions definit dans contributors
    author_user = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='Contributors',
                                         related_name="contributions")

    class Meta:
        verbose_name = "Projet"

    def __str__(self):
        return self.title


ROLE_CHOICES = (
    ('Author', 'Auteur'),
    ('Contributor', 'Contributeur'),
)


class Contributors(models.Model):
    """table through permettant d'établir la relation plusieurs-à-plusieurs
     entre la table Users et la table Projects"""
    # Table through : https://docs.djangoproject.com/fr/3.2/topics/db/models/
    # user_id(IntegerField)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    # project_id(IntegerField)
    project = models.ForeignKey(to=Projects,
                                on_delete=models.SET_NULL, null=True)
    # permission(ChoiceField)
    # permission = models.ChoiceField
    # role(CharField)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')

    class Meta:
        verbose_name = "Contributeur"


PRIORITY = (('Low', 'Faible'), ('Medium', 'Moyenne'),
            ('High', 'Elevée'))

TAG = (('Bug', 'Bug'), ('Improvement', 'Amélioration'),
       ('Task', 'Tâche'))

STATUS = (('To do', 'A faire'), ('In progress', 'En cours'),
          ('Finished', 'Terminé'))


class Issues(models.Model):
    """stocke tous les problèmes d'un projet, ainsi que leurs statut, priorité,
     attributaire (utilisateur auquel le problème est affecté), balise
      (bug, tâche, amélioration), et d'autres détails nécessaires mentionnés
       dans la table. Elle a une relation plusieurs-à-un avec la table Projects,
        et une autre relation plusieurs-à-un avec la table Users"""
    # title(Charfield)
    title = models.CharField(max_length=128, verbose_name="Titre")
    # desc(CharField)
    desc = models.CharField(max_length=200)
    # tag(CharField)
    tag = models.CharField(max_length=30, choices=TAG)
    # priority(CharField)
    priority = models.CharField(max_length=30, choices=PRIORITY)
    # project_id(InterField)
    project = models.ForeignKey(to=Projects,
                                on_delete=models.SET_NULL, null=True)
    # status(CharField)
    status = models.CharField(max_length=30, choices=STATUS)
    # author_user_id(ForeignKey)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                    on_delete=models.SET_NULL, null=True, related_name='author_by')
    # assignee_user_id(ForeignKey) Utilisateur auquel le problme est affecté
    assignee_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.SET_NULL, null=True,
                                      related_name='assignment')
    # created_time(DateTimeField)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Afficher les derniers dépôts en premier
        ordering = ['-created_time']
        # Affiche un nom autre que Issues
        verbose_name = "Problèmes recensé"

    def __str__(self):
        return self.title


class Comments(models.Model):
    """stocke tous les commentaires d'un problème particulier,
     et a donc une relation plusieurs-à-un avec la table Issues.
      Chaque commentaire contient des détails tels que description,
       user_id (relation plusieurs-à-un avec la table Users)"""
    # description(CharField)
    description = models.CharField(max_length=500)
    # author_user_id(ForeignKey)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                    on_delete=models.SET_NULL, null=True)
    # issue_user_id(ForeignKey)
    issue = models.ForeignKey(to=Issues,
                              on_delete=models.CASCADE)
    # created_time(DateTimeField)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commentaire"
