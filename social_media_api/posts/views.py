from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import permissions.IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post, Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
        

@api_view(['POST'])
def like_post(request, pk):
    """Handle liking a post using get_or_create."""
    post = generics.get_object_or_404(Post, pk=pk)

    # Use get_or_create to handle liking a post
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create a notification for the post owner
    notification = Notification.objects.create(
        recipient=post.user,  # Notify the post owner
        actor=request.user,
        verb='liked your post',
        target=post,
        target_content_type=ContentType.objects.get_for_model(Post),
        target_object_id=post.id
    )

    return Response({"detail": "Post liked successfully!"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def unlike_post(request, pk):
    """Handle unliking a post."""
    post = generics.get_object_or_404(Post, pk=pk)

    # Try to get the like object
    like = Like.objects.filter(user=request.user, post=post).first()

    if not like:
        return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    like.delete()

    return Response({"detail": "Post unliked successfully!"}, status=status.HTTP_200_OK)

        
