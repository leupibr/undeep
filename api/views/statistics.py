import glob
import os

from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def storage(request):
    doc_files = glob.glob(default_storage.base_location + '*')
    documents = sum([os.stat(f).st_size for f in doc_files if os.path.isfile(f)])

    index = _get_size_recursive(default_storage.base_location + 'index')
    model = _get_size_recursive(default_storage.base_location + 'category')

    return Response({
        'documents': documents,
        'index': index,
        'model': model
    })


def _get_size_recursive(index_dir):
    index_files = []
    for r, d, f in os.walk(index_dir):
        for file in f:
            index_files.append(os.path.join(r, file))
    index = sum([os.stat(f).st_size for f in index_files if os.path.isfile(f)])
    return index

