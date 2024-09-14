from django.contrib.auth.models import User
from rest_framework import serializers
from core.models import *
from rest_framework.authtoken.models import Token
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        # Ensure passwords match
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        # Set password and save user
        user.set_password(password)
        user.save()

        # Create token for the user
        Token.objects.create(user=user)

        return user

