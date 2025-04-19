from django.core.management.base import BaseCommand
from django.core import serializers

from property_managment.models import Property


class Command(BaseCommand):
    help = 'Custom dumpdata with specified encoding'

    def handle(self, *args, **kwargs):

        data = serializers.serialize('json', Property.objects.all())

        # Write to a file with specific encoding
        with open('fixtures/Property.json', 'w', encoding='utf-8') as f:
            f.write(data)