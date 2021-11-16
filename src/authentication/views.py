from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from authentication.serializers import UsersSerializer

# Create your views here.


@api_view(['POST', ])
def signup_view(request):

    if request.method == 'POST':
        serializer = UsersSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Nouvel utilisateur enregistré avec succès'
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.errors
        return Response(data)
