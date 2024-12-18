from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

# Ensure this field is explicitly specified as required
token_field = serializers.CharField()

# Ensure this field is explicitly specified as required
password_field = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    token = token_field  # Create the token field
    password = password_field  # Create the password field for write access

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'password', 'token']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)  # Get the password from validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],  # Set the user's password
            bio=validated_data.get('bio', ''),
        )
        token = Token.objects.create(user=user)  # Create a token for the user
        validated_data['token'] = token.key  # Include the token key in the validated data
        return validated_data
