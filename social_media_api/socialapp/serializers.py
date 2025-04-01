from rest_framework import serializers
from .models import User, Post, Comment, Like

# Create Serializers here 
class UserSerializer(serializers.ModelSerializer):
    model = User 
    fields = ['id', 'username', 'bio', 'profile_pic', 'followers', 'following']


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer():
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment 
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like 
        fields = '__a;ll__'