from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ArticleDocumentView



urlpatterns = [
    path('search/' ,ArticleDocumentView.as_view({'get': 'list'})),
]


