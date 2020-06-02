import datetime
import os
import tarfile

import pandas
import shutil

from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from api.models import Document, Category


class Command(BaseCommand):
    help = 'Loads a CSV file and add all documents to the storage'

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '-c', '--csv', help='Path to the CSV containing a list of documents to add',
        )
        group.add_argument(
            '-t', '--tar', help='Path to the TAR containing a documents and a index.csv',
        )

    def handle(self, *args, **options):
        if options.get('tar'):
            self.handle_tar(*args, **options)
        if options.get('csv'):
            self.handle_csv(*args, **options)

    def handle_tar(self, tar, *args, **options):
        imported = []
        uploaded = datetime.datetime.now(tz=datetime.timezone.utc)
        with tarfile.open(tar, 'r:*') as tar:
            file = tar.extractfile('index.csv')
            df = pandas.read_csv(file)
            columns = list(df.columns.values)
            for index, row in df.iterrows():
                category, _ = Category.objects.get_or_create(name=row.category)

                tar.extract(row.path, path=default_storage.base_location)

                doc = dict(zip(columns, row.values.tolist()))
                doc['category'] = category

                doc = Document.create(uploaded=uploaded, **doc)
                doc.save()
                doc.refresh_from_db(fields=['date', 'uploaded', 'modified'])
                imported.append(doc)
                self.stdout.write(self.style.NOTICE(f'* {doc.name} imported'))

        self.stdout.write(self.style.NOTICE(f'* indexing imported documents'))
        Document.index_multiple(imported)
        self.stdout.write(self.style.SUCCESS('documents successful imported'))

    def handle_csv(self, csv, *args, **options):
        csv_dir = os.path.dirname(os.path.abspath(csv))
        uploaded = datetime.datetime.now(tz=datetime.timezone.utc)

        df = pandas.read_csv(csv)
        columns = list(df.columns.values)
        imported = []
        for index, row in df.iterrows():
            category, c = Category.objects.get_or_create(name=row.category)
            path = os.path.join(csv_dir, row.path)

            filename = os.path.basename(path)
            target_path = os.path.join(default_storage.base_location, filename)

            shutil.copyfile(path, target_path)

            doc = dict(zip(columns, row.values.tolist()))
            doc['category'] = category
            doc['path'] = filename

            doc = Document.create(uploaded=uploaded, **doc)
            doc.save()
            doc.refresh_from_db(fields=['date', 'uploaded', 'modified'])
            imported.append(doc)
            self.stdout.write(self.style.NOTICE(f'* {filename} imported'))

        self.stdout.write(self.style.NOTICE(f'* indexing imported documents'))
        Document.index_multiple(imported)
        self.stdout.write(self.style.SUCCESS('documents successful imported'))
