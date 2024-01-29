
from rest_framework import serializers



class ArticleDocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    titre = serializers.CharField(read_only=True)
    resume = serializers.CharField(read_only=True)
    texteIntegral = serializers.CharField(read_only=True)
    motsCles = serializers.CharField(read_only=True)
    urlPdf=serializers.URLField(read_only=True)
    dateDePublication=serializers.DateField(read_only=True)
    references=serializers.CharField(read_only=True)
    auteurs=serializers.CharField(read_only=True)
    traiter=serializers.BooleanField(read_only=True)
   



    class Meta:
        fields = (
            'id',
            'titre',
            'resume',
            'texteIntegral',
            'motsCles',
            'urlPdf',
            'dateDePublication',
            'references',
            'auteurs',
            'traier',
            
        )
      
 
  