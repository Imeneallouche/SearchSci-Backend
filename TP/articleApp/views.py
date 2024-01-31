from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import json
import requests
from .documents import *
from .serializers import *
from .models import Article


from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
)


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

@api_view(['GET'])
def get_Upload_List(request): #Affiche la liste des titres des articles uploadés non vérifiés
 if request.method=='GET':
   articlesUploades = Article.objects.filter(traiter=False)
   serializer = ArticleTitleSerializer(articlesUploades,many=True)
   return Response ({"Articles Uploadés":serializer.data})

@api_view(['GET'])
def get_Article_Details(request, id):
    try:
       article = Article.objects.get(pk=id)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer = ArticleSerializer(article)
        return Response({"Détails de l'article":serializer.data})


@api_view(['DELETE'])
def delete_Article(request, id):
    try:
       article = Article.objects.get(pk=id)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






    

  




# def generate_random_data():
#     url = 'https://newsapi.org/v2/everything?q=tesla&from=2023-11-25&sortBy=publishedAt&apiKey=b976da46a1ac45eb868d27e210bfa0ee'
#     r = requests.get(url)
#     payload = json.loads(r.text)
#     count = 1
#     for data in payload.get('articles'):
#         print(count)
#         ElasticDemo.objects.create(
#             title = data.get('title'),
#             content = data.get('description')
#         )

# def index(request):
#     generate_random_data()
#     return JsonResponse({'status' : 200})







# class PublisherDocumentView(DocumentViewSet):
#     document = NewsDocument
#     serializer_class = NewsDocumentSerializer
#     lookup_field = 'first_name'
#     fielddata=True
#     filter_backends = [
#         FilteringFilterBackend,
#         OrderingFilterBackend,
#         CompoundSearchFilterBackend,
#     ]
   
#     search_fields = (
#         'title',
#         'content',
#     )
#     multi_match_search_fields = (
#        'title',
#         'content',
#     )
#     filter_fields = {
#        'title' : 'title',
#         'content' : 'content',
#     }
#     ordering_fields = {
#         'id': None,
#     }
#     ordering = ( 'id'  ,)
        
  