from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)  # Add this line for the token field
    password = serializers.CharField(write_only=True)  # Mark this field as write-only

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'password', 'token']  # Include the token field in the list of fields
        extra_kwargs = {'password': {'write_only': True}}  # Specify that the password is write-only

    def create(self, validated_data):
        password = validated_data.pop('password', None)  # Extract password from validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=password,  # Assign password after creating user
            bio=validated_data.get('bio', ''),
        )
        token, _ = Token.objects.get_or_create(user=user)  # Create or retrieve the token
        validated_data['token'] = token.key  # Assign token to validated data
        return validated_data
