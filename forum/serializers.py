from rest_framework import serializers
from .models import ForumPost, ForumComment, ForumReply

class ForumReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumReply
        fields = '__all__'

class ForumCommentSerializer(serializers.ModelSerializer):
    replies = ForumReplySerializer(many=True, read_only=True)

    class Meta:
        model = ForumComment
        fields = '__all__'

class ForumPostSerializer(serializers.ModelSerializer):
    comments = ForumCommentSerializer(many=True, read_only=True)

    class Meta:
        model = ForumPost
        fields = '__all__'
