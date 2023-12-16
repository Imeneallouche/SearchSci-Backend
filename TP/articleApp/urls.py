
from django.urls import path
from . import views

urlpatterns = [
    path('articles/',views.get_all_Articles,name='articles' ),
    path('articles/<str:pk>/',views.get_by_id_Articles,name='article_by_id' ),
]