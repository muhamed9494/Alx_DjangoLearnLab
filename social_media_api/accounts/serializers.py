from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'following']  # Include any other fields you need


User = get_user_model()

# Create a CharField explicitly for serializer use
password_field = serializers.CharField(write_only=True)
serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)  # This creates the token field
    password = password_field  # Create the password field for write access

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'password', 'token']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    # Method to create a user with the specified data and generate a token
    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],  # Set the user's password
            bio=validated_data.get('bio', ''),
        )
        token = Token.objects.create(user=user)  # Create a token for the user
        validated_data['token'] = token.key  # Add the token key to the validated data
        return validated_data
