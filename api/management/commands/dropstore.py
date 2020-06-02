import glob
import os
import shutil

from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from api.models import Document


class Command(BaseCommand):
    help = 'Drops the complete store, index and cleans the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '-y', '--yes', help='Skip warning and drop all documents',
            action='store_false', dest='show_warning'
        )

    def handle(self, *args, **options):
        if options['show_warning']:
            self.stdout.write(self.style.WARNING('This command will drop all documents irrevocable!'))
            response = input('do you really want to delete all data? [y/N] ')

            if response.lower() not in {'y', 'yes'}:
                self.stdout.write(self.style.SUCCESS('phew... operation cancelled'))
                return

        index_dir = os.path.join(default_storage.base_location, 'index')
        self.stdout.write(self.style.NOTICE('* deleting index'))
        shutil.rmtree(index_dir, ignore_errors=True)

        category_dir = os.path.join(default_storage.base_location, 'category')
        self.stdout.write(self.style.NOTICE('* deleting model'))
        shutil.rmtree(category_dir, ignore_errors=True)

        self.stdout.write(self.style.NOTICE('* remove database entries'))
        Document.objects.all().delete()

        self.stdout.write(self.style.NOTICE('* deleting files'))
        files = glob.glob(default_storage.base_location + '/*')
        for f in files:
            if os.path.isfile(f):
                os.remove(f)

        self.stdout.write(self.style.SUCCESS('storage successfully dropped'))
