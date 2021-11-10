from rest_framework.serializers import ModelSerializer

from alert.models import Projects



class ProjectsSerializer(ModelSerializer):
    """Serialize la classe Projects"""

    class Meta:
        model = Projects
        fields = ['title', 'description', 'type', 'author_user']
