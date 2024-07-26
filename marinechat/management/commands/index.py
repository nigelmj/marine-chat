from django.core.management.base import BaseCommand
from marinechat.utils import load_documents, split_documents, store_documents

class Command(BaseCommand):
    help = 'Index and embed documents'

    def handle(self, *args, **kwargs):
        docs = load_documents()
        all_splits = split_documents(docs)
        store_documents(all_splits)
