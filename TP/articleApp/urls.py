
from django.urls import path
from . import views

urlpatterns = [
    path('articles/',views.get_all_Articles,name='articles' ),
    path('articles/<str:pk>/',views.get_by_id_Articles,name='article_by_id' ),
    # path('index/',views.index,name='articles' ),
   
    # path('search/' ,views.PublisherDocumentView.as_view({'get': 'list'})),

    path('uploadList/',views.get_Upload_List,name='uploadList' ),
    path('detailsArticle/<int:id>/',views.get_Article_Details,name='detailsArticle' ),
    path('deleteArticle/<int:id>/',views.delete_Article,name='deleteArticle' ),


]