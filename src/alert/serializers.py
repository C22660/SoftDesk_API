from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from alert.models import Projects, Contributors, Issues


class ProjectsListSerializer(ModelSerializer):
    """Serialize la classe Projects"""

    class Meta:
        model = Projects
        fields = ['title', 'description']

    # Vérification que le titre n'existe pas déjà en cas de création d'un nouveau projet
    def validate_title(self, value):
        if Projects.objects.filter(title=value).exists():
            raise serializers.ValidationError('Project already exists')
        return value


class ContributorsSerializer(ModelSerializer):
    """Serialize la classe Contributors"""


    class Meta:
        model = Contributors
        fields = ['user', 'project', 'role']


class ProjectsDetailSerializer(ModelSerializer):
    """Serialize la classe Projects"""

    # Plutôt que d'afficher 'author_user' dans les fields, on affiche plus de détail quant à
    # la contribution en affectant un related_name 'contributeur' à la foreignkey du mondel
    # Contributors (lien avec Projects), puis on l'ajoute dans les fields à afficher.
    # Pour ne pas avoir simplement les ID, on repasse le sérializer de Contributors avec le
    # paramètre many=True
    contributeur = ContributorsSerializer(many=True)

    class Meta:
        model = Projects
        fields = ['title', 'description', 'type', 'contributeur']


class IssuesSerializer(ModelSerializer):
    """Serialize la classe Issues"""

    class Meta:
        model = Issues
        fields = ['title', 'desc', 'tag', 'priority', 'status', 'assignee_user', 'created_time']
