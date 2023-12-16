from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
     class Meta:
          model = Article
          fields="__all__"
          #fields= ['titre','resume','texte_integral','mots_cles','URL_Pdf','auteurs','references']