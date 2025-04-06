from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, generics, status
from .models import User, Post, Comment, Like 
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.decorators import action, api_view
from rest_framework.response import Response 
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes 
from django.urls import reverse 
from django.conf import settings 
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
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


def send_notifications(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {"type": "send_notification", "message": message}
    )

# Handle password reset request (Sends email reset link)
@api_view(['POST'])
def password_reset_request(request):
    email = request.data.get('email')
    try:
        user = get_user_model().objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User with this email does not exist.'}, status=400)

    # Generate reset token and UID 
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

    # Send email
    subject = "Password Reset Request"
    message = f"Hi {user.username}, \n You requested a new password.\n Click the link to reset your password: {reset_url} \n If you did not request this, please ignore this email."

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    return JsonResponse({'message': 'Password email sent if email exists.'}, status=200)


# Confirm password resets (Allows user to reset password)
@api_view(['POST'])
def password_reset_confirm(request, uidb64, token):
    try:
        uid =  urlsafe_base64_decode(uidb64).decode()  
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist):
        return JsonResponse({'error': 'Invalid reset link.'}, status=400)

    if default_token_generator.check_token(user, token):
        new_password = request.data.get('new_password1')
        confirm_password = request.data.get('new_password2')

        if new_password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        user.set_password(new_password)
        user.save()
        return JsonResponse({'message': 'Password reset successful'}, status=200)

    return JsonResponse({'error': 'Invalid token or expired link'}, status=400)


class DeleteAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk=None):
        user = request.user
        user.delete()
        return Response({'detail': 'Account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)