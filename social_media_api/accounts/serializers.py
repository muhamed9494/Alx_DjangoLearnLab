from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)  # Create the token field
    password = serializers.CharField(write_only=True)  # Create the password field for write access

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'password', 'token']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],  # Set the user's password
            bio=validated_data.get('bio', ''),
        )
        token = Token.objects.create(user=user)  # Create a token for the user
        validated_data['token'] = token.key  # Include the token key in the validated data
        return validated_data
