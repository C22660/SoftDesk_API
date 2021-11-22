from rest_framework import serializers, request
from rest_framework.serializers import ModelSerializer

from alert.models import Projects, Contributors, Issues, Comments


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

    def create(self, project=None):

        contributor = Contributors(
            user=self.validated_data['user'],
            role=self.validated_data['role'],
            project=project
        )
        contributor.save()
        # Resérialization de contributor pour qu'il puisse être affiché, en Json, par le
        # httpResponse de la view
        contributor_serialized = ContributorsSerializer(instance=contributor).data

        return contributor_serialized

class ProjectsDetailSerializer(ModelSerializer):
    """Serialize la classe Projects"""

    # Plutôt que d'afficher 'author_user' dans les fields, on affiche plus de détail quant à
    # la contribution en affectant un related_name 'contributeur' à la foreignkey du mondel
    # Contributors (lien avec Projects), puis on l'ajoute dans les fields à afficher.
    # Pour ne pas avoir simplement les ID, on repasse le sérializer de Contributors avec le
    # paramètre many=True
    contributeur = ContributorsSerializer(many=True, read_only=True)

    class Meta:
        model = Projects
        fields = ['title', 'description', 'type', 'contributeur']


class IssuesSerializer(ModelSerializer):
    """Serialize la classe Issues"""

    class Meta:
        model = Issues
        fields = ['title', 'desc', 'tag', 'priority', 'status', 'author_user', 'assignee_user',
                  'created_time']

    def create(self, project=None):

        issue = Issues(
            project=project,
            title=self.validated_data['title'],
            desc=self.validated_data['desc'],
            tag=self.validated_data['tag'],
            priority=self.validated_data['priority'],
            status=self.validated_data['status'],
            author_user=self.validated_data['author_user'],
            assignee_user=self.validated_data['assignee_user'],
        )
        issue.save()

        # Resérialization de issue pour qu'il puisse être affiché, en Json, par le
        # httpResponse de la view
        issue_serialized = IssuesSerializer(instance=issue).data

        return issue_serialized


class CommentsSerializer(ModelSerializer):
    """Serialize la classe Comments"""

    class Meta:
        model = Comments
        fields = ['issue', 'description', 'author_user', 'created_time']

    def create(self, issue_concerned=None):

        comment = Comments(
            issue=issue_concerned,
            description=self.validated_data['description'],
            author_user=self.validated_data['author_user'],
        )
        comment.save()

        # Resérialization de comment pour qu'il puisse être affiché, en Json, par le
        # httpResponse de la view
        comment_serialized = CommentsSerializer(instance=comment).data

        return comment_serialized
