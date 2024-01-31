from rest_framework import serializers
from .models import Article
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer



class ArticleSerializer(serializers.ModelSerializer):
     class Meta:
          model = Article
          fields="__all__"
          #fields= ['titre','resume','texte_integral','mots_cles','URL_Pdf','auteurs','references']


class UtilisateurSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    favoris = ArticleSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        # Customize the representation of the instance
        return {
            'email': instance.user.email,
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'favoris': ArticleSerializer(instance.Favoris.all(), many=True).data,
            # Add more fields as needed
        }

