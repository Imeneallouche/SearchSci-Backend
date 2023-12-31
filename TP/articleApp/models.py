from django.db import models


#done
class Reference(models.Model):
    titre = models.TextField( default='',blank=False)
    
    def __str__(self):
       return self.titre
    
#done
class Institution(models.Model):
    nom = models.CharField(max_length=100,default='',blank=False)
    adress = models.TextField(default='',blank=True)#meme le pays inclus

    def __str__(self):
       return self.nom


#done
class Auteur(models.Model):
    full_name= models.CharField(max_length=200,default='', blank=False)
    institution=models.ForeignKey(Institution, null=True, on_delete=models.SET_NULL)
    email=models.EmailField(blank=True)

    def __str__(self):
       return f"{self.full_name}"
    
    @property
    def institution_indexing(self):
        if self.institution is not None:
            return {self.institution.nom,
                    self.institution.adress,}
    

class Article(models.Model):
    titre = models.CharField(max_length=100,default='',blank=False)
    resume = models.TextField(default='',blank=True)
    texte_integral = models.TextField( default='',blank=True)
    mots_cles= models.CharField(max_length=1000, default='',blank=True)
    URL_Pdf = models.URLField(max_length=200, default='',blank=False)
    auteurs= models.ManyToManyField(Auteur)
    references=models.ManyToManyField(Reference)
    traiter=models.BooleanField(default=False)
    

    def __str__(self):
       return self.titre
    
    @property
    def references_indexing(self):
        return [reference.title for reference in self.references.all()]
    
    @property
    def Auteurs_indexing(self):
        return [
           {auteur.full_name, auteur.email, auteur.institustion }  for auteur in self.auteurs.all()
            ]

       

  


    
