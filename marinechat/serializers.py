from rest_framework import serializers
from .models import Message, Citation, Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file']

class CitationSerializer(serializers.ModelSerializer):
    source = DocumentSerializer()

    class Meta:
        model = Citation
        fields = ['id', 'source', 'quote']

class MessageSerializer(serializers.ModelSerializer):
    citations = CitationSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'message', 'timestamp', 'user', 'citations']
