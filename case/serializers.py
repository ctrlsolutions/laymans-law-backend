from rest_framework import serializers
from .models import Case, CaseAttachment, Comment
from django.contrib.auth import get_user_model
from user.models import CustomUser

from user.serializers import NestedUserSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'first_name', 'last_name', 'email', 'contact_number']

class CaseSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = serializers.SerializerMethodField()  
    class Meta:
        model = Case
        fields = (
            'id',
            'title',
            'description',
            'created_by',
            'assigned_to',
            'status',
            'case_type',
            'created_date',
            'accepted_date',
            'image', 
            'video',
            'document',
            'attachments',
        )
        read_only_fields = ('created_by', 'assigned_to', 'created_date', 'accepted_date', 'status')
        extra_kwargs = {
            'created_by': {'read_only': True},  # Let the view handle this
        }

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

    def get_video(self, obj):
        if obj.video:
            return self.context['request'].build_absolute_uri(obj.video.url)
        return None
    
    def get_attachments(self, obj):
        attachments = obj.attachments.all()
        return CaseAttachmentSerializer(
            attachments, 
            many=True,
            context={'request': self.context['request']}  # Pass request context
        ).data

    def create(self, validated_data):
        user = self.context['request'].user  
        validated_data['created_by'] = user
        return super().create(validated_data)

class CaseAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField() 
    class Meta:
        model = CaseAttachment
        fields = ('id', 'case', 'file', 'file_url', 'uploaded_at', 'description')
        read_only_fields = ('case', 'uploaded_at')

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file:
            return request.build_absolute_uri(obj.file.url)
        return None
    
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'case', 'author', 'content', 'created_at', 'is_lawyer')
        read_only_fields = ('author', 'created_at', 'is_lawyer')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        validated_data['is_lawyer'] = request.user.is_lawyer()  # Assuming you have this field
        return super().create(validated_data)