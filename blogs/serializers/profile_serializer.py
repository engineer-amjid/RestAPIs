from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Profile
        fields = ['user_id', 'username', 'first_name', 'last_name', 'image', 'last_login']
