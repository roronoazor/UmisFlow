from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, CreateUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from authentication.authentication import BearerTokenAuthentication

User = get_user_model()

# Create your views here.
class LoginView(generics.CreateAPIView):
    
    def post(self, request, *args, **kwargs):
        
        user = User.objects.filter(
            username=request.data.get("username")
        ).first()

        if not user:
            user = User.objects.create(
                username=request.data.get("username"),
                password=request.data.get("password"),
                email=request.data.get("username"),
                is_active=True
            )
            user.set_password(request.data.get("password"))
            user.save()
        
        # if the user is not active throw error
        if not user.is_active:    
            return response.Response({'detail': 'authentication failed'}, status=status.HTTP_400_BAD_REQUEST)    
        
        # if password does not match 
        if not user.check_password(request.data.get('password')):
            return response.Response({'detail': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)    
        
        # delete all previous tokens
        Token.objects.filter(user=user).delete()
        
        # create a new token for that user
        token = Token.objects.create(user=user)
        
        data = dict()
        data['user'] = UserSerializer(user).data
        data['token'] = token.key
        
        return response.Response(data, status=status.HTTP_201_CREATED)
    

class LogoutView(generics.CreateAPIView):
    
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        tokens = Token.objects.filter(user=request.user)
        # delete all tokens affiliated with this user
        tokens.delete()
        return response.Response({'detail': 'Logout Successful'}, status=status.HTTP_200_OK)
