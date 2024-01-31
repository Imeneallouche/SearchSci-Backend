from rest_framework import serializers
from .models import *
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import *


class ReferenceSerializer(serializers.ModelSerializer):
     class Meta:
          model = Reference
          exclude = ['id']

class InstitutionSerializer(serializers.ModelSerializer):
     class Meta:
          model = Institution
          exclude = ['id']

class AuteurSerializer(serializers.ModelSerializer):
     institution = InstitutionSerializer()
     class Meta:
          model = Auteur
          exclude = ['id']

class ArticleSerializer(serializers.ModelSerializer):
     references = ReferenceSerializer(many=True)
     auteurs = AuteurSerializer(many=True)
     class Meta:
          model = Article
          #fields="__all__"
          fields= ['titre','resume','texte_integral','mots_cles','URL_Pdf','auteurs','references']

class ArticleTitleSerializer(serializers.ModelSerializer):
     titre = serializers.CharField()
     class Meta:
          model = Article
          fields = ['titre']

# # class NewsDocumentSerializer(DocumentSerializer):

#     class Meta(object):
#         """Meta options."""
#         model = ElasticDemo
#         document = NewsDocument
#         fields = (
#             'title',
#             'content',
#         )
#         def get_location(self, obj):
#             """Represent location value."""
#             try:
#                 return obj.location.to_dict()
#             except:
#                 return {}
            



        