from django.contrib import auth
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = auth.authenticate(request, username=username, password=password)
    if user:
        auth.login(request, user)
        token = Token.objects.get_or_create(user=user)[0]
        return Response({'user': username, 'token': token.pk}, status.HTTP_200_OK)
    return Response({'message': 'Invalid username or password'}, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    auth.logout(request)
    return Response(None, status.HTTP_204_NO_CONTENT)

