from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ForumPost, ForumPostBookmark

User = get_user_model()

class ForumPostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    bookmark_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ForumPost
        fields = ['id', 'author', 'title', 'content', 'timestamp', 'category', 'bookmark_count', 'updated_at']
        read_only_fields = ['author', 'timestamp', 'updated_at']

    def get_author(self, obj):
        return {
            'user_id': obj.author.user_id,
            'first_name': obj.author.first_name,
            'last_name': obj.author.last_name
        }

class ForumPostBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumPostBookmark
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['user', 'created_at']
