from rest_framework import serializers
from .models import (Product, Cart)
from django.contrib.auth import get_user_model

User = get_user_model()

# my serializer classes


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cart
		fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'


class ResendEmailSerializer(serializers.Serializer):
	email = serializers.CharField()
