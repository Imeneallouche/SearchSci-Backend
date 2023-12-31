import json

from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import ArticleDocument

class ArticleDocumentSerializer(DocumentSerializer):
    class Meta:
        # Specify the correspondent document class
        document = ArticleDocument

        # List the serializer fields. Note, that the order of the fields
        # is preserved in the ViewSet.
        fields = (
            'id',
            'titre',
            'resume',
            'mots_cle',
            'texte_integral',
            'URL_Pdf',
            'auteurs',
            'references',
        )