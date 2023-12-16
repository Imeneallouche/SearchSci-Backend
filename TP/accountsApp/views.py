from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Moderateur,Utilisateur
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SingUpSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout , login as dj_login

# Create your views here.    



    
'''--------------------------------------------------------------------------------------
    Regetration: pour les trois users:
        1:Administrateur: avec la commande createsuperuser
        2:Moderateur: la fonction Add_Moderateur
        3:Utilisateur: la fonction register_Utilisateur
--------------------------------------------------------------------------------------'''

## Register: Client: Utilisateur simple 
@api_view(['POST'])
def register_Utilisateur(request):
    data = request.data
    user1 = SingUpSerializer(data = data)

    if user1.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user2 = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'], 
                email = data['email'] , 
                username = data['email'] , 
                password = make_password(data['password']),
            )
            utilisateur=Utilisateur.objects.create(user=user2)
            return Response(
                {'details':'Your account Utilisateur registered susccessfully!' },
                    status=status.HTTP_201_CREATED
                    )
        else:
            return Response(
                {'eroor':'This email already exists!' },
                    status=status.HTTP_400_BAD_REQUEST
                    )
    else:
        return Response(user1.errors)


## Add Moderateur: une fonctionnalité 3and l'administrateur==Resiter Moderateur
@api_view(['POST'])
def Add_Moderateur(request):
    data = request.data
    user1 = SingUpSerializer(data = data)

    if user1.is_valid():
        if not User.objects.filter(username=data['email']).exists():   #l'unicité de l'email doit etre global 
            user2 = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'], 
                email = data['email'] , 
                username = data['email'] , 
                password = make_password(data['password']),
             
            )
            moderateur=Moderateur.objects.create(user=user2)
            return Response(
                {'details':'Your account Moderateur registered susccessfully!' },
                    status=status.HTTP_201_CREATED
                    )
        else:
            return Response(
                {'eroor':'This email already exists!' },
                    status=status.HTTP_400_BAD_REQUEST
                    )
    else:
        return Response(user1.errors)
'''--------------------------------------------------------------------------------------
    Login: pour les trois users:
        1:Administrateur: redirect vers 
        2:Moderateur: 
        3:Utilisateur: 
--------------------------------------------------------------------------------------'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def redirect_loggedin_user(request):

    user = request.user
    utilisateur_exists = Utilisateur.objects.filter(user_id=user.id).exists()
    moderateur_exists = Moderateur.objects.filter(user_id=user.id).exists()

    if user.is_staff:
        return Response({'user': 'administrateur'})

    if moderateur_exists:
        moderateur = Moderateur.objects.get(user=user)
        return Response({'user': 'Moderateur'})

    if utilisateur_exists:
        utilisateur = Utilisateur.objects.get(user=user)
        return Response({'user': 'utilisateur'})
    
    return Response({'user': 'Non trouvé'})