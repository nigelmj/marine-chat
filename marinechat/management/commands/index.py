from django.core.management.base import BaseCommand
from marinechat.utils import index_documents

class Command(BaseCommand):
    help = 'Index and embed documents'

    def handle(self, *args, **kwargs):
        index_documents()
