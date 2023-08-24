from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'address']

    def create(self, validated_data):
        company = Company.objects.create(**validated_data)
        return company