from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from .views import ArticleDocumentView



urlpatterns = [
    path('search/' ,ArticleDocumentView.as_view({'get': 'list'})),
    path('upload/', views.process_folder_link),
    path('test/', views.test)

]


