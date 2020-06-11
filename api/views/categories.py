import re
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Category, Document
from api.views.documents import _render_documents


@api_view()
def categories(request):
    data = Category.objects\
        .all()\
        .order_by('name')

    return Response([
        {
            'name': c.name,
            'count': c.document_set.count(),
            'predictions': c.document_set.filter(method=Document.AUTO).count()
        } for c in data])


@api_view()
def count(request):
    return Response(Category.objects.all().count())


@api_view()
def random(request):
    from random import choice
    names = {'Avalanche', 'Blizzard', 'Cyclone', 'Dream', 'Earthquake', 'Hailstorm', 'Hurricane', 'Illusion',
             'Nightmare', 'Ocean', 'Snowstorm', 'Storm', 'Tempest', 'Thunder', 'Thunderstorm', 'Tornado', 'Twister',
             'Typhoon', 'Vision', 'Wave', 'Windstorm', 'Arbiter', 'Breaker', 'Broker', 'Catcher', 'Discoverer',
             'Examiner', 'Explorer', 'Finder', 'Guide', 'Inspector', 'Mediator', 'Patrol', 'Pioneer', 'Precursor',
             'Procurer', 'Scout', 'Searcher', 'Surfer', 'Thrower', 'Vanguard'}
    free_names = list(names - set(Category.objects.values_list('name', flat=True)))
    return Response(choice(free_names))


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def category(request, name):
    if request.method == 'GET':
        c = get_object_or_404(Category, name=name)
        return Response(
            {
                'name': c.name,
                'count': c.document_set.count(),
                'predictions': c.document_set.filter(method=Document.AUTO).count()
            }
        )

    if request.method in ('POST', 'PUT'):
        item, created = Category.objects.update_or_create(name=name)
        if created:
            return Response(None, status.HTTP_201_CREATED)

        if request.data.get('name'):
            name = request.data.get('name', name)
            if not re.match(r'^(\w{1,10})(?<!^_random$)$', name):
                return Response({'message': 'Bad name provided!'}, status.HTTP_400_BAD_REQUEST)
            item.name = name
            item.save()

        return Response(None, status.HTTP_204_NO_CONTENT)

    if request.method == 'DELETE':
        c = get_object_or_404(Category, name=name)
        c.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def assign(request, name):
    c = get_object_or_404(Category, name=name)
    d = get_object_or_404(Document, path=request.data.get('document'))
    d.category = c
    d.method = Document.MANUAL
    d.save()
    d.index('category')
    return Response(None, status.HTTP_204_NO_CONTENT)


@api_view()
def documents(request, name, offset=0, limit=None):
    c = get_object_or_404(Category, name=name)
    offset = int(offset)
    limit = int(limit)
    count = c.document_set.count()
    range = slice(offset, offset + (limit or count))
    docs = c.document_set.order_by('-uploaded')[range]

    return Response({
        'total': count,
        'documents': _render_documents(docs)
    })
