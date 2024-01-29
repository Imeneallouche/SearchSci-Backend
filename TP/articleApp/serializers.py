from rest_framework import serializers
from .models import Article
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer





class ArticleSerializer(serializers.ModelSerializer):
     class Meta:
          model = Article
          fields="__all__"
          #fields= ['titre','resume','texte_integral','mots_cles','URL_Pdf','auteurs','references']



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
            



        