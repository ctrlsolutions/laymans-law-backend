# case/serializers.py
from rest_framework import serializers
from .models import Case

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'
        read_only_fields = ['created_by']

    def create(self, validated_data):
        # Automatically attach the logged-in user to the case
        user = self.context['request'].user  # Get the user from the request context
        validated_data['created_by'] = user
        return super().create(validated_data)
