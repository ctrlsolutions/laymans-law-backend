from rest_framework import serializers
from .models import Case, CaseAttachment
from django.contrib.auth import get_user_model

from user.serializers import NestedUserSerializer

User = get_user_model()

class CaseSerializer(serializers.ModelSerializer):
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

    def get_attachments(self, obj):
        return CaseAttachmentSerializer(obj.attachments.all(), many=True).data

    def create(self, validated_data):
        user = self.context['request'].user  
        validated_data['created_by'] = user
        return super().create(validated_data)

class CaseAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseAttachment
        fields = ('id', 'case', 'file', 'uploaded_at', 'description')
        read_only_fields = ('case', 'uploaded_at') # Case might be set based on URL