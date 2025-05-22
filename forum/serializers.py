from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ForumPost

User = get_user_model()

class ForumPostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = ForumPost
        fields = ['id', 'author', 'title', 'content', 'timestamp', 'category', 'bookmark']
        read_only_fields = ['author', 'timestamp']

    def get_author(self, obj):
        return {
            'first_name': obj.author.first_name,
            'last_name': obj.author.last_name
        }
