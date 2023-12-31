
from django.urls import path
from . import views

urlpatterns = [

    path('login/',views.redirect_loggedin_user,name='login'),
    path('register_utilisateur/',views.register_Utilisateur,name='register_utilisateur'),
    path('ajouter_moderateur/',views.Add_Moderateur,name='ajouter_moderateur'),
    path('supprimer_moderateur/', views.SupprimerModerateur, name='supprimer_moderateur'),
    path('modifier_moderateur/', views.ModifierModerateur, name='modifier_moderateur'),
    path('afficher_moderateur/', views.AfficherModerateur, name='afficher_moderateur'),
    path('afficher_moderateurs/', views.AfficherModerateurs, name='afficher_moderateurs'),
     #------------extra------------------
    path('supprimer_user/', views.SupprimerUser, name='supprimer_user'),
    path('userinfo/',views.current_user,name='user_info'),
    path('afficher_utilisateur/', views.AfficherUtilisateur, name='afficher_utilisateur'), 
    path('afficher_utilisateurs/', views.AfficherUtilisateurs, name='afficher_utilisateurs'),
    path('afficher_users/', views.AfficherUsers, name='afficher_users'),
     ]