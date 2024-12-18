from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'password', 'token']

    def create(self, validated_data):
        password = validated_data.pop('password', None)  # Retrieve password from validated data
        user = User.objects.create_user(**validated_data)  # Create user with remaining fields
        if password:
            user.set_password(password)  # Set the password
            user.save()  # Save the user with the new password
        token, _ = Token.objects.get_or_create(user=user)  # Create or retrieve token for user
        validated_data['token'] = token.key  # Add token to validated data
        return validated_data



