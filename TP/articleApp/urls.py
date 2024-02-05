
from django.urls import path
from . import views

urlpatterns = [
    path('articles/',views.get_all_Articles,name='articles' ),
    path('articles/<str:pk>/',views.get_by_id_Articles,name='article_by_id' ),
    path('supprimer_article/<str:pk>/',views.supprimer_Article,name='supprimer_Article' ),
    path('addToFavorites/<str:pk>/',views.add_to_favorites,name='addToFavorites' ),
    path('removeFromFovoris/<str:pk>/',views.remove_from_favorites,name='remove_from_favorites' ),
    path('IsInFavorites/<str:pk>/',views.is_article_in_favorites,name='is_article_in_favorites' ),

    path('favorites/',views.view_favorites,name='favorites' ),
    path('Rectifier_Article/',views.rectifierArticle,name='rectifierArticle'),
]