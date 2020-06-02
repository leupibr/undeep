import os

from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from api.models import Document


class Command(BaseCommand):
    help = 'Initializes the `whoosh` index and schema'

    def add_arguments(self, parser):
        parser.add_argument(
            '-y', '--yes', help='Skip warning to drop document',
            action='store_false', dest='show_warning'
        )
        parser.add_argument('document', help='Document to be dropped')

    def handle(self, *args, **options):
        if options['show_warning']:
            self.stdout.write(self.style.WARNING('This command will drop the given document irrevocable!'))
            response = input('do you really want to delete all data? [y/N] ')

            if response.lower() not in {'y', 'yes'}:
                self.stdout.write(self.style.SUCCESS('phew... operation cancelled'))
                return

        document = Document.objects.filter(path=options['document'])[0]

        self.stdout.write(self.style.NOTICE('* deleting index'))
        document.de_index()

        self.stdout.write(self.style.NOTICE('* remove database entries'))
        document.delete()

        self.stdout.write(self.style.NOTICE('* deleting file'))
        path = os.path.join(default_storage.base_location, document.path)
        os.remove(path)

        self.stdout.write(self.style.SUCCESS('document successfully dropped'))
