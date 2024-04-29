from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data['password']
        password2 = validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error': 'Passwords do not match'})

        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'User with email already exists'})

        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=password
        )

        return user
