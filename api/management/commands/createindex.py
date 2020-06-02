import os

from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from whoosh.fields import Schema, ID, TEXT, DATETIME
from whoosh.index import create_in

from api.models import Document


class Command(BaseCommand):
    help = 'Initializes the `whoosh` index and schema'

    def handle(self, *args, **options):
        index_dir = os.path.join(default_storage.base_location, 'index')

        if not os.path.exists(index_dir):
            os.mkdir(index_dir)

        self.stdout.write(self.style.NOTICE('* recreating index'))
        # TODO: add correct fields to schema
        #       * labels
        schema = Schema(
            path=ID(stored=True, unique=True),
            name=TEXT(stored=True),
            category=TEXT(stored=True),
            content=TEXT(stored=True),
            date=DATETIME(stored=True),
            uploaded=DATETIME(stored=True))
        create_in(index_dir, schema)

        self.stdout.write(self.style.NOTICE('* reindexing documents'))
        Document.index_multiple(Document.objects.all())

        self.stdout.write(self.style.SUCCESS('index created'))
