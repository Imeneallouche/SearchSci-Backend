from django.contrib import admin
from.models import Administrateur,Moderateur,Utilisateur

# Register your models here.
admin.site.register(Administrateur)
admin.site.register(Moderateur)
admin.site.register(Utilisateur)