from django.core.management.base import BaseCommand

from api.scan import scan


class Command(BaseCommand):
    help = 'Scans a document from the attach scanner, and imports it into the database'

    def handle(self, *args, **options):
        scan()
