from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.management import call_command


@api_view(['GET'])
def recreate_index(request):
    call_command('createindex')
    return Response(None, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def learn_categories(request):
    call_command('learn', 'category')
    return Response(None, status=status.HTTP_204_NO_CONTENT)

