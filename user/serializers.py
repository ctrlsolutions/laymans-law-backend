from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate


from rest_framework import serializers
from django.db import IntegrityError
from .models import CustomUser, Lawyer

class SignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

    roll_number = serializers.IntegerField(required=False, allow_null=True)
    roll_signed_date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            "first_name", "last_name", "email", "contact_number",
            "gender", "birth_date", "password", "confirm_password",
            "user_type", "roll_number", "roll_signed_date"
        ]

    def validate(self, data):
        """Custom validation to check password match and Lawyer-specific fields"""
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        if data["user_type"] == "lawyer":
            if not data.get("roll_number") or not data.get("roll_signed_date"):
                raise serializers.ValidationError({
                    "lawyer_info": "Roll number and roll signed date are required for lawyers."
                })
        else:
            data.pop("roll_number", None)
            data.pop("roll_signed_date", None)
        
        return data

    def create(self, validated_data):
        """Create a CustomUser and Lawyer if needed"""
        validated_data.pop("confirm_password")
        
        user_type = validated_data.pop("user_type")
        roll_number = validated_data.pop("roll_number", None)  
        roll_signed_date = validated_data.pop("roll_signed_date", None)

        user = CustomUser.objects.create_user(**validated_data, user_type=user_type)

        if user_type == "lawyer" and roll_number and roll_signed_date:
            Lawyer.objects.create(user=user, roll_number=roll_number, roll_signed_date=roll_signed_date)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("testing Invalid email or password.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
        else:
            raise serializers.ValidationError("Both email and password are required.")
        
        data['user'] = user
        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "contact_number", "gender", "birth_date", "user_type"]
        read_only_fields = ["email", "user_type"]  # Prevent modification of email & user_type

    def update(self, instance, validated_data):
        """Update only the provided fields"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance