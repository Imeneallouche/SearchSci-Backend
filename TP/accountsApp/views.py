
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Moderateur,Utilisateur
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SingUpSerializer,UserSerializer,UserSerializer2, UserSerializer3
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout , login as dj_login
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes


  
'''--------------------------------------------------------------------------------------
    Registration: pour les trois users:
        1:Administrateur: avec la commande createsuperuser
        2:Moderateur: la fonction Add_Moderateur
        3:Utilisateur: la fonction register_Utilisateur
--------------------------------------------------------------------------------------'''
@extend_schema(
    request=SingUpSerializer,  # Specify the serializer for the request body
    responses={
        201: OpenApiResponse(description="Your account Utilisateur registered successfully"),
        400: OpenApiResponse(description="This email already exists or invalid data provided"),
    }
)
## Register_Utilisateur: Client: Utilisateur simple 
@api_view(['POST'])
def register_Utilisateur(request):
    """
    Register_Utilisateur: register a simple Utilisateur.

    Registers a simple Utilisateur based on the provided data.

    """
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


#___________________________________________________#

@extend_schema(
    request=SingUpSerializer,  # Specify the serializer for the request body
    responses={
        201: OpenApiResponse(description="Your account Moderateur registered successfully"),
        400: OpenApiResponse(description="This email already exists or invalid data provided"),
    }
)
## Add Moderateur: une fonctionnalité chez l'administrateur==Register Moderateur
@api_view(['POST'])
def Add_Moderateur(request):
    """
    Add_Moderateur: register a Moderateur.

    Adds a Moderateur based on the provided data.

    """
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
@extend_schema(
    description="Retrieve information about the currently authenticated user.",
    responses={200: UserSerializer}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Retrieve information about the currently authenticated user.

    Returns details about the currently authenticated user.

    """ 
    user = UserSerializer(request.user, many=False)
    return Response(user.data)

@extend_schema(
    request= UserSerializer3,
    responses={
        200: OpenApiTypes.OBJECT,
        403: OpenApiResponse(description="User not found"),
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def redirect_loggedin_user(request):
    """
    Redirects logged-in user to appropriate page based on their role.

    Retrieves the user's role (administrateur, Moderateur, utilisateur) and returns the appropriate response.
    
    """
   
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

'''--------------------------------------------------------------------------------------
    Gestion des modérateurs: 
        1:supprimer modérateur
        2:modifier moderateur 
        3:afficher moderateur
        4:afficher moderateurs
--------------------------------------------------------------------------------------'''
@extend_schema(
    responses={
        204: OpenApiResponse(description="No content. Moderateur deleted successfully."),
        400: OpenApiResponse(description='Error. Email parameter is required in the request data.'),
        404: OpenApiResponse(description="Moderateur not found ."),
    }
)
## 1:supprimer_moderateur
@api_view(['DELETE'])
def SupprimerModerateur(request):
    """
    Deletes a Moderateur based on the email.

    """
    data = request.data

    try:
        email = data.get('email', None)  # Filtrage par email
        if email is None:
            return Response({'error': 'Email parameter is required in the request data.'}, status=status.HTTP_400_BAD_REQUEST)

        user1 = User.objects.get(email=email)
        Moderateur.objects.get(user=user1).delete()
        User.objects.get(email=email).delete()

        return Response({'details': 'Moderateur deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Moderateur.DoesNotExist:
        return Response({'error': 'Moderateur not found.'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    responses={
        200: OpenApiResponse(description="Moderateur updated successfully."),
        400: OpenApiResponse(description='Error. Email parameter is required in the request data.'),
        404: OpenApiResponse(description="Moderateur not found."),
    }
)
## 2:modifier_moderateur
@api_view(['PUT'])
def ModifierModerateur(request):
    """
    Modify a Moderateur.

    Modifies a Moderateur based on the email and data.

    """
    data = request.data
    try:
        email = data.get('email', None)
        if email is None:
            return Response({'error': 'Email parameter is required in the request data.'}, status=status.HTTP_400_BAD_REQUEST)

        user_instance = User.objects.get(email=email)
        moderateur_instance = Moderateur.objects.get(user=user_instance)

        # Update user fields
        user_instance.first_name = data.get('first_name', user_instance.first_name)
        user_instance.last_name = data.get('last_name', user_instance.last_name)
      # Add other feilds : 
      #  user_instance.last_name = data.get('password', user_instance.password)
      #  user_instance.last_name = data.get('email', user_instance.email)
        user_instance.save()
      #  moderateur_instance.save()

        return Response({'details': 'Moderateur updated successfully!'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Moderateur.DoesNotExist:
        return Response({'error': 'Moderateur not found.'}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    responses={
        200: UserSerializer2,
        400: OpenApiResponse(description='Error. Email parameter is required in the request data.'),
        404: OpenApiResponse(description="Moderateur not found."),
    }
)    
## 3:Afficher un moderateur par email
@api_view(['GET'])
def AfficherModerateur(request):
    """
    Retrieve information about a specific Moderateur.

    Returns details about the specified Moderateur.

    """
    try:
        email = request.data.get('email', None)

        if email is None:
            return Response({'error': 'Email parameter is required in the request data.'}, status=status.HTTP_400_BAD_REQUEST)

        user1 = User.objects.filter(username=email).first()

        if not user1:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        moderateur = Moderateur.objects.filter(user=user1).first()

        if not moderateur:
            return Response({'error': 'Moderateur not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Return specific fields directly
        serializer = UserSerializer2(moderateur)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    responses={
     200: UserSerializer2(many=True),
     404: OpenApiResponse(description="No Moderateurs found."),
     }
)
## 4:Afficher touts les moderateurs de l'app web 
@api_view(['GET'])
def AfficherModerateurs(request):
    """
    Retrieve information about all Moderateurs.

    Returns details about all Moderateurs registered in the system.

    """
    try:
        # Retrieve all Moderateurs
        moderateurs = Moderateur.objects.all()

        if not moderateurs:
            return Response({'error': 'No Moderateurs found.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the list of Moderateurs
        serializer = UserSerializer2(moderateurs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    




'''  _______________________extra____________________________'''

@extend_schema(
    responses={
        200: UserSerializer2,
        400: OpenApiResponse(description='Error. Email parameter is required in the request data.'),
        404: OpenApiResponse(description="User not found."),
    }
)    
 ## Afficher un utilisateur par son email    
@api_view(['GET'])
def AfficherUtilisateur(request):
    """
    Retrieve information about a specific Utilisateur

    """
    try:
        email = request.data.get('email', None)

        if email is None:
            return Response({'error': 'Email parameter is required in the request data.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        utilisateur = Utilisateur.objects.get(user=user)

        if not Utilisateur:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Return specific fields directly
        serializer = UserSerializer2(utilisateur)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    responses={
     200: UserSerializer2(many=True),
     404: OpenApiResponse(description="No Utilisateurs found."),
     }
)   
@api_view(['GET'])
def AfficherUtilisateurs(request):
    """
    Retrieve information about all Utilisateurs.

    Returns details about all Utilisateurs registered in the system.

    """
    try:
        # Retrieve all users
        utilisateurs = Utilisateur.objects.all()

        # Serialize the list of users
        serializer = UserSerializer2(utilisateurs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@extend_schema(
    responses={
     200: UserSerializer3(many=True),
     500: OpenApiResponse(description="Internal Server Error."),
     }
)
## Display all users : Admin/moder/utilis
@api_view(['GET'])
def AfficherUsers(request):
    """
    Retrieve information about all Users: Admins, Moderateurs and Utilisateurs.

    """
    try:
        # Retrieve all users
        users = User.objects.all()

        # Serialize the list of users
        serializer = UserSerializer3(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    responses={
        204: OpenApiResponse(description="No content. User deleted successfully."),
        400: OpenApiResponse(description='Error. Email parameter is required in the request data.'),
        404: OpenApiResponse(description="User not found ."),
    }
)    
## Delete a user (in general) par email
@api_view(['DELETE'])
def SupprimerUser(request):
    """
    Deletes a User based on the email.
    
    """
    data = request.data

    try:
        email = data.get('email', None)  # Filtrage par email
        if email is None:
            return Response({'error': 'Email parameter is required in the request data.'}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.filter(email=email).delete()
    
        return Response({'details': 'User deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)





