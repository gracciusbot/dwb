from rest_framework import serializers
from BlogApp.models import Post, Follow, Comment, Profile
from django.contrib.auth.models import User

# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    class Meta:
        model = Profile
        fields = ['id', 'user', 'photo', 'bio', 'followers_count']
        read_only_fields = ['user']

# User Serializer 
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)  # Relacionamento com o Profile
    profile_photo = serializers.ImageField(source='profile.photo', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'profile_photo_url']


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Representa o autor pelo nome de usuário
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())  # Relaciona ao post

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at']
        read_only_fields = ['created_at']

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # Comentários do post
    author_photo_url = serializers.ImageField(source='author.profile.photo', read_only=True)  # Acessa a foto através do profile do autor
    author = serializers.StringRelatedField() 
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'subscription', 'photo_post', 'author', 'created_at', 'updated_at', 'likes_count', 'comments', 'author_photo_url']  # Usando 'author_photo_url' ao invés de 'author_photo'



# Follow Serializer
class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ['follower', 'following']




class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']