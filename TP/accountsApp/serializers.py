
from rest_framework import serializers
from django.contrib.auth.models import User


class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'password')

        extra_kwargs = {
            'first_name': {'required':True ,'allow_blank':False},
            'last_name' : {'required':True ,'allow_blank':False},
            'email' : {'required':True ,'allow_blank':False},
            'password' : {'required':True ,'allow_blank':False,'min_length':4}
        }



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'username') 
        
        
# On utilise  UserSerializer2   dans les requete specifiant un type precie de users ,
# weather :  Administrateur / moderateur / utilisateur  
     
class UserSerializer2(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    # Add more fields as needed

    def to_representation(self, instance):
        # Customize the representation of the instance
        return {
            'email': instance.user.email,
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            # Add more fields as needed
        }
        
 # On utilise  UserSerializer3   dans les requete liee aux users in general      
class UserSerializer3(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    # Add more fields as needed

    def to_representation(self, instance):
        # Customize the representation of the instance
        return {
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            # Add more fields as needed
        }


