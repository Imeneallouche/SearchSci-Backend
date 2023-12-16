from django.db import models

# Create your models here.

class Reference(models.Model):
    titre = models.CharField(max_length=100, default='',blank=False)
    type_reference = models.CharField(max_length=100, choices=(
        ('Livre', 'Livre'),
        ('Article de journal', 'Article de journal'),
        ('Conférence', 'Conférence'),
           ))
    def __str__(self):
       return self.titre
    


class Institution(models.Model):
    nom = models.CharField(max_length=100,default='',blank=False)
    pays = models.CharField(max_length=1000,default='',blank=False)
    adresse = models.TextField(default='',blank=False)

   
    def __str__(self):
       return self.nom

class Auteur(models.Model):
    nom= models.CharField(max_length=100,default='', blank=False)
    prenom= models.CharField(max_length=100,default='',blank=False)
    institution=models.ForeignKey(Institution, null=True, on_delete=models.SET_NULL)

    def __str__(self):
       return f"{self.nom} {self.prenom}"
    


class Article(models.Model):
    titre = models.CharField(max_length=100,default='',blank=False)
    resume = models.TextField(default='',blank=False)
    texte_integral = models.TextField( default='',blank=False)
    mots_cles= models.CharField(max_length=1000, default='',blank=False)
    URL_Pdf = models.URLField(max_length=200, default='',blank=False)
    auteurs= models.ManyToManyField(Auteur)
    references=models.ManyToManyField(Reference)
    # null=True: esq ces champs sont necessaires ou non

    def __str__(self):
       return self.titre

    


    
