from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer
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
