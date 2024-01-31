from django.db import models
from django.contrib.auth.models import User
from articleApp.models import  Article


# Create your models here.

class Administrateur(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
      return f"{self.user.first_name} {self.user.last_name}"
      

class Moderateur(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
      return f"{self.user.first_name} {self.user.last_name}"


class Utilisateur(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Favoris= models.ManyToManyField(Article)

    def __str__(self):
      return f"{self.user.first_name} {self.user.last_name}"
