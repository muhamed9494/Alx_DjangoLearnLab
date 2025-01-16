from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import CustomUser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer

# Follow User - Ensures user is authenticated and adds the follow relationship
class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Ensures user must be authenticated

    def post(self, request, user_id):
        # Get the user to follow
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        
        # Add the following relationship (one-way)
        request.user.following.add(user_to_follow)
        
        return Response({"message": f"User {user_to_follow.username} followed successfully!"})

# Unfollow User - Ensures user is authenticated and removes the follow relationship
class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Ensures user must be authenticated

    def post(self, request, user_id):
        # Get the user to unfollow
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        
        # Remove the following relationship
        request.user.following.remove(user_to_unfollow)
        
        return Response({"message": f"User {user_to_unfollow.username} unfollowed successfully!"})

# List all users - This view lists all users (optional, for demonstration or admin use)
class ListUsersView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Ensures user must be authenticated

    def get(self, request):
        users = CustomUser.objects.all()
        # Serialize the user data (this will depend on your CustomUser serializer)
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id})
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id})
        return Response({'error': 'Invalid credentials'}, status=400)





