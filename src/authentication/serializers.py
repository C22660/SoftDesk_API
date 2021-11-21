from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from authentication.models import Users
# from SoftDesk import settings


class UsersSerializer(ModelSerializer):
    """Serialize la classe Users pour la création d'un utilisateur"""
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # pour s'assurer que password et passorwd2 matchent, on overwrite la méthode save
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Les mots de passe doivent être identiques'})
        # user = Users.objects.create_user(email=self.validated_data['email'],
        #                           username=self.validated_data['username'],
        #                           password=password
        #                           )
        user = Users(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user
        # pourtant, dans la doc https://www.django-rest-framework.org/api-guide/serializers/
        # Additional keyword arguments

        # user = Users(
        #     email=self.validated_data['email'],
        #     username=self.validated_data['username'],
        #     password=password,
        # )
        # user.save()
        # return user

