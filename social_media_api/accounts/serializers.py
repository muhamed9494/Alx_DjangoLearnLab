from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)  # Token field for read access
    password = serializers.CharField(write_only=True)  # Password field for write access

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'password', 'token']
        extra_kwargs = {
            'password': {'write_only': True}  # Mark password as write-only
        }

    def create(self, validated_data):
        # Extract password from validated data
        password = validated_data.pop('password', None)

        # Create a user using the provided data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=password,  # Assign the password
            bio=validated_data.get('bio', ''),
        )

        # Create a token for the user
        token, _ = Token.objects.get_or_create(user=user)

        # Return the user with the token included in the validated data
        validated_data['token'] = token.key
        return validated_data
