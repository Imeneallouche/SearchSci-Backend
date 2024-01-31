from django.shortcuts import render,get_object_or_404
from .models import Article
from .serializers import ArticleSerializer,UtilisateurSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accountsApp.models import Utilisateur
# Create your views here.


@api_view(['PUT','GET','DELETE','POST'])
def get_all_Articles(request):
    articles=Article.objects.all()
    serializer=ArticleSerializer(articles,many=True)
    print(articles)
    return Response ({"Articles":serializer.data})

@api_view(['PUT','GET','DELETE','POST'])
def get_by_id_Articles(request,pk):
    article=get_object_or_404(Article,id=pk)
    serializer=ArticleSerializer(article,many=False)
    print(article)
    return Response ({"Article":serializer.data})


## version1
@api_view(['GET'])
def afficher_details_article(request,pk):
    article = get_object_or_404(Article, id=pk)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)

## version2
@api_view(['GET'])
def afficher_details_article(request):
    article_id = request.data.get('article_id', None)

    if article_id is None:
        return Response({'error': 'Article ID is required in the request data.'}, status=status.HTTP_400_BAD_REQUEST)

    article = get_object_or_404(Article, id=article_id)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favorites(request):
    article_id = request.data.get('article_id')   # Fix: Added missing parentheses and quotes
    print(request.user)
    print(article_id)
    print("----------------------------------------")
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

