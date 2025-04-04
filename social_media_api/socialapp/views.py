from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import User, Post, Comment, Like 
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response 

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'bio']

    # Implementing follow/unfollow logic
    @action(detail=True, methods=['POST'])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        if user_to_follow != request.user:
            request.user.following.add(user_to_follow)
            return Response({'status': 'followed'})
        return Response({'status': 'You cannnot follow yourself'})

    @action(detail=True, methods=['POST'])    
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()
        request.user.following.remove(user_to_unfollow)
        return Response({'status': 'unfollowed'})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permissions_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['content', 'user__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]