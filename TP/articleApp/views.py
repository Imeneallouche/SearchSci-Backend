from django.shortcuts import render,get_object_or_404
from .models import Article
from .serializers import ArticleSerializer,UtilisateurSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accountsApp.models import Utilisateur
from .models import Article, Auteur, Reference, Institution


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

## réctifier article
@api_view(['PUT'])
def rectifierArticle(request):
    data = request.data
    article_data = data.get('Article', None)
    pk = article_data.get('id', None)

    if pk is not None:
        try:
            article_instance = Article.objects.get(pk=pk)

            # Mise à jour des champs de l'article
            article_instance.titre = article_data.get('titre', article_instance.titre)
            article_instance.texteIntegral = article_data.get('texteIntegral', article_instance.texteIntegral)
            article_instance.resume = article_data.get('resume', article_instance.resume)
            article_instance.motsCles = article_data.get('motsCles', article_instance.motsCles)
            article_instance.urlPdf = article_data.get('urlPdf', article_instance.urlPdf)
            article_instance.traiter = article_data.get('traiter', article_instance.traiter)

            # Enregistrer les modifications de l'article
            article_instance.save()

            # Mise à jour des références de l'article
            references_data = article_data.get('references', [])
            references = [Reference.objects.get_or_create(titre=ref_data['titre'])[0] for ref_data in references_data]
            article_instance.references.set(references)

            # Mise à jour des auteurs de l'article
            auteurs_data = article_data.get('auteurs', [])
            auteurs = []
            for auteur_data in auteurs_data:
                institution_data = auteur_data.get('institution', {})
                institution, _ = Institution.objects.get_or_create(nom=institution_data.get('nom', ''),
                                                                    adress=institution_data.get('adress', ''))
                auteur, _ = Auteur.objects.get_or_create(full_name=auteur_data.get('full_name', ''),
                                                          email=auteur_data.get('email', ''),
                                                          institution=institution)
                auteurs.append(auteur)
            article_instance.auteurs.set(auteurs)

            return Response({"Article": "Mise à jour réussie"})
        except Article.DoesNotExist:
            return Response({"Article": "L'article n'existe pas"}, status=404)
    else:
        return Response({"Article": "ID de l'article non fourni"}, status=400)
