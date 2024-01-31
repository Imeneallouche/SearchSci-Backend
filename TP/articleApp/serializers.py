from rest_framework import serializers
from .models import Article,Auteur,Reference,Institution
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer


class InstitutionSerializer(serializers.ModelSerializer):
   class Meta: 
      model=Institution
      fields=['nom','adress']


class AuteurSerializer(serializers.ModelSerializer):
      full_name=serializers.CharField(read_only=True)
      institution=InstitutionSerializer(read_only=True)
      email=serializers.EmailField(read_only=True)
    
      def to_representation(self, instance):
        return {
             'full_name':instance.full_name,
             'email':instance.email,
             'institution':InstitutionSerializer(instance.institution).data,
             
        }

   
class ReferenceSerializer(serializers.ModelSerializer):
   class Meta: 
      model=Reference
      fields=['titre']



class ArticleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    titre = serializers.CharField(read_only=True)
    resume = serializers.CharField(read_only=True)
    texteIntegral = serializers.CharField(read_only=True)
    motsCles = serializers.CharField(read_only=True)
    urlPdf=serializers.URLField(read_only=True)

    references=ReferenceSerializer(many=True, read_only=True)
    auteurs=AuteurSerializer(many=True, read_only=True)
    traiter=serializers.BooleanField(read_only=True)


    def to_representation(self, instance):
        return {
             'id':instance.id,
             'titre':instance.titre,
             'resume':instance.resume,
             'texteIntegral':instance.texteIntegral,
             'motsCles':instance.motsCles,
             'urlPdf':instance.urlPdf,
             'references':ReferenceSerializer(instance.references.all(),many=True).data,
             'auteurs':AuteurSerializer(instance.auteurs.all(),many=True).data,
             'traiter': instance.traiter, 
        }
    
    

     
      

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

