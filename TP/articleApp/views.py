from django.shortcuts import render,get_object_or_404
from .models import Article
from .serializers import ArticleSerializer,UtilisateurSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accountsApp.models import Utilisateur


#afficher tout les article
@api_view(['PUT','GET','DELETE','POST'])
def get_all_Articles(request):
    articles=Article.objects.all()
    serializer=ArticleSerializer(articles,many=True)
    return Response ({"Articles":serializer.data})


#afficher détails article
@api_view(['PUT','GET','DELETE','POST'])
def get_by_id_Articles(request,pk):
    article=get_object_or_404(Article,id=pk)
    serializer=ArticleSerializer(article,many=False)
    return Response ({"Article":serializer.data})

#supprimer article
@api_view(['PUT','GET','DELETE','POST'])
def supprimer_Article(request,pk):
    try:
        Article.objects.get(id=pk).delete()
        return Response({'details': 'Article deleted successfully!'}, status=status.HTTP_200_OK)
    except Article.DoesNotExist:
        return Response({'error': 'Article not found.'}, status=status.HTTP_404_NOT_FOUND)


#ajouter article to favoris
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favorites(request, article_id):
    try:
        utilisateur = Utilisateur.objects.get(user=request.user)
        article = Article.objects.get(pk=article_id)
        utilisateur.Favoris.add(article)
        utilisateur.save()
        return Response({'details': 'Article added to favorites successfully!'}, status=status.HTTP_200_OK)
    except Article.DoesNotExist:
        return Response({'error': 'Article not found.'}, status=status.HTTP_404_NOT_FOUND)


## consulter Favoris
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_favorites(request):
    utilisateur = Utilisateur.objects.get(user=request.user)
    serializer = UtilisateurSerializer(utilisateur)
    return Response(serializer.data, status=status.HTTP_200_OK)

