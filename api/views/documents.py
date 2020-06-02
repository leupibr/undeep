import datetime
import json
import os
import uuid

from dateutil.parser import parse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin
from whoosh.qparser.dateparse import DateParserPlugin

from api.models import Document
from api.scan import scan as scan_document


@api_view(['GET'])
def count(request):
    return Response(Document.objects.all().count())


@api_view(['GET'])
def recent(request, order=None, offset=0, limit=10):
    offset = int(offset or 0)
    limit = int(limit or 10)
    count = Document.objects.all().count()
    range = slice(offset, offset + (limit or count))
    order = {'modified': ['-modified'], 'uploaded': ['-uploaded']} \
        .get(order, ['-modified', '-uploaded'])
    order += ['name']
    result = Document.objects.order_by(*order)[range]
    return Response({
        'total': count,
        'documents': _render_documents(result)
    })


@api_view(['POST'])
def upload(request):
    uploaded = datetime.datetime.now(tz=timezone.utc)

    stored = _store_files(request)
    documents = [Document.create(uploaded=uploaded, **item) for item in stored]
    Document.predict_multiple(documents)
    for doc in documents:
        doc.save()
    Document.index_multiple(documents)
    return Response(_render_documents(documents), status=status.HTTP_201_CREATED)


@login_required
def download(request, path):
    document = get_object_or_404(Document, path=path)
    file_path = os.path.join(default_storage.base_location, document.path)

    response = HttpResponse(open(file_path, 'rb'), content_type='application/pdf')
    if request.path.strip('/').endswith('download'):
        response['Content-Disposition'] = f'attachment; filename={document.name}.pdf'
    else:
        response['Content-Disposition'] = f'filename={document.name}.pdf'
    return response


@api_view(['GET'])
def search(request):
    term = request.GET.get('q')
    if not term:
        return Response('Invalid search term', status=status.HTTP_400_BAD_REQUEST)

    index_dir = os.path.join(default_storage.base_location, 'index')
    if not os.path.exists(index_dir):
        return Response('Index not initialized', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    ix = open_dir(index_dir)
    with ix.searcher() as searcher:
        parser = MultifieldParser(['name', 'content'], ix.schema)
        parser.add_plugin(FuzzyTermPlugin())
        parser.add_plugin(DateParserPlugin(free=True))

        query = parser.parse(term)
        result = searcher.search(query)
        results = [r['path'] for r in result]

    documents = Document.objects.filter(path__in=results)
    return Response(_render_documents(documents))


@api_view(['POST'])
def scan(request):
    doc = scan_document()
    return Response(_render_documents([doc]), status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST', 'DELETE'])
def index(request, path):
    document = get_object_or_404(Document, path=path)

    if request.method == 'GET':
        # TODO: fix localization and timezone stuff
        return Response({
            'name': document.name,
            'path': document.path,
            'date': document.date,
            'alt_dates': document.find_dates(),
            'uploaded': document.uploaded.isoformat(),
            'modified': document.modified.isoformat(),
            'size': document.size,
            'category': document.category.name if document.category else None,
            'method': document.get_method_display()
        })

    if request.method == 'DELETE':
        document.de_index()
        document.delete()
        os.remove(document.get_storage_path())
        return HttpResponse(status=204)

    if request.method == 'POST':
        document.name = request.data.get('name', document.name)
        if request.data.get('date'):
            document.date = parse(request.data['date']).date()
        document.save()
        document.index('name')
        return Response(None, status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def confirm(request, path):
    document = get_object_or_404(Document, path=path)
    if document.method == Document.MANUAL:
        return Response('Category is manually set and cannot be accepted', status=status.HTTP_400_BAD_REQUEST)
    if document.method == Document.CONFIRMED:
        return Response('Category is already confirmed', status=status.HTTP_400_BAD_REQUEST)

    document.method = Document.CONFIRMED
    document.save()
    return Response(None, status=status.HTTP_204_NO_CONTENT)


def _store_files(request):
    uploaded = []

    for _, file in request.FILES.items():
        path = f'{uuid.uuid4()}'
        with default_storage.open(path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        uploaded.append(dict(name=file.name, path=path))
    return uploaded


def _index_documents(documents: [Document]):
    index_dir = os.path.join(default_storage.base_location, 'index')
    if not os.path.exists(index_dir):
        return Response('Index not initialized', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    ix = open_dir(index_dir)
    writer = ix.writer()
    for doc in documents:
        doc.index(writer)
    writer.commit()


def _render_documents(documents: [Document]):
    return [{
        'name': r.name,
        'path': r.path,
        'size': r.size,
        'category': r.category.name,
        'date': r.date,
        'method': r.get_method_display(),
        'uploaded': r.uploaded,
        'modified': r.modified,
    } for r in documents]
