from rest_framework import serializers
from .models import Case
from django.contrib.auth import get_user_model

from user.serializers import NestedUserSerializer

User = get_user_model()

class CaseSerializer(serializers.ModelSerializer):
    created_by = NestedUserSerializer(read_only=True)
    assigned_to = NestedUserSerializer(read_only=True, allow_null=True)
    class Meta:
        model = Case
        fields = (
            # 'id',
            'title',
            'description',
            'created_by',
            'assigned_to',
            'status',
            'case_type',
            'created_date',
            'accepted_date',
        )
        read_only_fields = ('created_by', 'assigned_to', 'created_date', 'accepted_date', 'status')

    def create(self, validated_data):
        user = self.context['request'].user  
        validated_data['created_by'] = user
        return super().create(validated_data)
