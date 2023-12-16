from django.contrib import admin

# Register your models here.
from .models import Article,Institution,Reference,Auteur

admin.site.register(Article)
admin.site.register(Auteur)
admin.site.register(Institution)
admin.site.register(Reference)
