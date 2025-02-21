from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'contact', 'gender', 'dateofbirth', 'rollno', 'rollsigneddate', 'password', 'confirm_password']

        def validate(self, data):
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError("Passwords do not match")
            return data
        
        def create(self, validated_data):
            user = CustomUser(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                sex=validated_data['sex'],
                birthdate=validated_data['birthdate'],
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
