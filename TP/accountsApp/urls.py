
from django.urls import path
from . import views

urlpatterns = [
    path('userinfo/',views.current_user,name='user_info'),
    path('register_utilisateur/',views.register_Utilisateur,name='register_utilisateur'),
    path('add_moderateur/',views.Add_Moderateur,name='add_moderateur'),
    path('login/',views.redirect_loggedin_user,name='login'),
]