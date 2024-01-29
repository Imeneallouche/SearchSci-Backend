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
    # texteIntegral = models.TextField( default='',blank=True)
    motsCles= models.CharField(max_length=1000, default='',blank=True)
    urlPdf = models.URLField(max_length=200, default='',blank=False)
    dateDePublication=models.DateField(null=True)
    auteurs= models.ManyToManyField(Auteur)
    references=models.ManyToManyField(Reference)
    traiter=models.BooleanField(default=False)
    

    def __str__(self):
       return self.titre
    






    @property
    def references_indexing(self):
        return [reference.titre for reference in self.references.all()]
    @property
    def auteurs_Institutions_indexing(self):
        return [[auteur.full_name, auteur.email, auteur.institution.nom, auteur.institution.adress]for auteur in self.auteurs.all()]
    @property
    def auteurs_indexing(self):
        return [[auteur.full_name, auteur.email]for auteur in self.auteurs.all()]
    @property
    def institutions_indexing(self):
        return [[auteur.institution.nom, auteur.institution.adress]for auteur in self.auteurs.all()]






    @property
    def texteIntegral(self):
      chemin_fichier = 'C:\\Users\\DELL\\Desktop\\TPIGL\\SearchSci-Backend\\TP\\TexteIntegral.txt'
      with open(chemin_fichier, 'r') as fichier:
        contenu = fichier.read()
        print(contenu)
        return contenu
      with open(chemin_fichier, 'w') as fichier:
        fichier.write('')
      print(contenu)
      return contenu
      




   


    


    @property
    def auteur_indexing(self):
        wrapper = dict_to_obj({
            'name': self.city.country.name,
            'city': {
                'name': self.city.name
            }
        })
        return wrapper

    @property
    def continent_indexing(self):
        wrapper = dict_to_obj({
            'name': self.city.country.continent.name,
            'country': {
                'name': self.city.country.name,
                'city': {
                    'name': self.city.name,
                }
            }
        })
        return wrapper