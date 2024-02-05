from django.db import models
from django_elasticsearch_dsl_drf.wrappers import dict_to_obj


class Reference(models.Model):
    titre = models.TextField( default='',blank=False)
    def __str__(self):
       return self.titre
    

class Institution(models.Model):
    nom = models.CharField(max_length=100,default='',blank=False)
    adress = models.TextField(default='',blank=True)#meme le pays inclus

    def __str__(self):
       return self.nom



class Auteur(models.Model):
    full_name= models.CharField(max_length=200,default='', blank=False)
    institution=models.ForeignKey(Institution, null=True, on_delete=models.SET_NULL)
    email=models.EmailField(blank=True)

    def __str__(self):
       return f"{self.full_name}"
    
    
    

class Article(models.Model):
    titre = models.CharField(max_length=100,default='',blank=False)
    resume = models.TextField(default='',blank=True)
    texteIntegral = models.TextField( default='',blank=True)
    motsCles= models.CharField(max_length=1000, default='',blank=True)
    urlPdf = models.URLField(max_length=200, default='',blank=False)
    dateDePublication=models.DateField(null=True)
    auteurs= models.ManyToManyField(Auteur)
    references=models.ManyToManyField(Reference)
    traiter=models.BooleanField(default=False)
    

    def __str__(self):
       return self.titre
    







   


    

