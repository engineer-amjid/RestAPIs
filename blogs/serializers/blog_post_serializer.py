from django.contrib.auth.models import User
from rest_framework import serializers
from blogs.models.blog_model import BlogPost

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
class BlogPostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'body', 'author']