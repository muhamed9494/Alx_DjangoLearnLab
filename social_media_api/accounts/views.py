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
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

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

@api_view(['POST'])
def follow_user(request, user_id):
    """Handle following a user."""
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    
    if user_to_follow == request.user:
        return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    
    request.user.following.add(user_to_follow)
    
    # Create a notification for the new follower
    notification = Notification.objects.create(
        recipient=user_to_follow,
        actor=request.user,
        verb="started following you",
        target=user_to_follow,
        target_content_type=ContentType.objects.get_for_model(CustomUser),
        target_object_id=user_to_follow.id
    )
    
    return Response({"detail": f"Now following {user_to_follow.username}"}, status=status.HTTP_200_OK)




