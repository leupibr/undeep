import csv
import os
import tarfile

from django.core.management.base import BaseCommand

from api.models import Document


class Command(BaseCommand):
    help = 'Dumps all documents into a TAR bundle include an CSV for later import'

    def add_arguments(self, parser):
        parser.add_argument('outfile', help='Output file to create')

    def handle(self, *args, **options):
        docs = Document.objects.all()

        # columns = 'path,name,date,category,method'
        with tarfile.open(options.get('outfile'), 'w:gz') as tar:
            with open('index.csv', 'w') as f:
                out = csv.writer(f)
                out.writerow(['path', 'name', 'date', 'category', 'method'])
                for doc in docs:
                    tar.add(doc.get_storage_path(), doc.path)
                    out.writerow((doc.path, doc.name, doc.date, doc.category.name, doc.method))
            tar.add('index.csv')
        os.remove('index.csv')
