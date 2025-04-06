from rest_framework import serializers
from .models import User, Post, Comment, Like

# Create Serializers here 
# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User 
        fields = ['id', 'username', 'bio', 'profile_image', 'followers_count', 'following_count', 'created_at']


# Serializer for Post Model
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


# Serializer for Comment Model
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment 
        fields = '__all__'


# Serializer for Like Model
class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like 
        fields = '__all__'