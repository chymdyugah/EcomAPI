from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import (permissions, generics, status)
from rest_framework.response import Response
from .filtersets import ShopFilterSet
from .models import (Product, Cart)
from .serializers import (ProductSerializer, CartSerializer, UserSerializer, ResendEmailSerializer)
from django.contrib.auth import get_user_model
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.account.admin import EmailAddress
from allauth.account.utils import send_email_confirmation
from rest_framework.exceptions import APIException


import datetime


User = get_user_model()

# Create your views here.


class Index(generics.ListAPIView):
	queryset = Product.objects.all()[0:12]
	serializer_class = ProductSerializer
	permission_classes = [permissions.AllowAny]

	def get(self, request, *args, **kwargs):
		products = self.get_queryset()
		serializer = self.serializer_class(products, many=True)
		if 'id' not in request.session:
			request.session['id'] = hash(datetime.datetime.now())

		cart = request.session['id']
		data = dict(products=serializer.data)
		data['cart'] = Cart.objects.filter(cart_id=cart, status='').count()
		data['cart_id'] = cart
		# print(data)
		return Response(data, status=status.HTTP_200_OK)


class Shop(generics.ListAPIView):
	queryset = Product.objects.all().order_by('id')
	serializer_class = ProductSerializer
	filter_class = ShopFilterSet
	permission_classes = [permissions.AllowAny]

	def get(self, request, *args, **kwargs):
		if 'id' not in request.session:
			request.session['id'] = hash(datetime.datetime.now())

		return super().get(request)

	def get_paginated_response(self, data):
		cart = self.request.session['id']
		serializer = dict(products=data)
		serializer['cart'] = Cart.objects.filter(cart_id=cart, status='').count()
		serializer['cart_id'] = cart
		return super().get_paginated_response(serializer)


class CartView(generics.ListAPIView):
	# queryset = Product.objects.all()
	serializer_class = CartSerializer
	permission_classes = [permissions.AllowAny]

	def get_queryset(self):
		cart = self.request.session['id']
		return Cart.objects.filter(cart_id=cart)

	def get(self, request, *args, **kwargs):
		if 'id' not in request.session:
			request.session['id'] = hash(datetime.datetime.now())

		cart = request.session['id']
		products = self.get_queryset()
		serializer = self.serializer_class(products, many=True)
		data = dict(products=serializer.data)
		data['cart'] = Cart.objects.filter(cart_id=cart, status='').count()
		data['cart_id'] = cart
		return Response(data, status=status.HTTP_200_OK)


class Single(generics.RetrieveAPIView):
	serializer_class = ProductSerializer
	queryset = Product.objects.all()
	permission_classes = [permissions.AllowAny]

	def get(self, request, *args, **kwargs):
		if 'id' not in request.session:
			request.session['id'] = hash(datetime.datetime.now())

		cart = request.session['id']
		prodid = kwargs.get('prodid', None)
		product = self.queryset.get(prodid=prodid)
		serializer = self.serializer_class(product)
		data = dict(product=serializer.data)
		data['cart'] = Cart.objects.filter(cart_id=cart, status='').count()
		data['cart_id'] = cart
		return Response(data, status=status.HTTP_200_OK)


class GoogleLogin(SocialLoginView):
	adapter_class = GoogleOAuth2Adapter


class FacebookLogin(SocialLoginView):
	adapter_class = FacebookOAuth2Adapter


"""
class NewEmailConfirmation(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self, request):
		email = request.data['email']
		user = get_object_or_404(User, email=request.data['email'])
		email_confirmed = EmailAddress.objects.fiter(user=user, verified=True).exists()

		if email_confirmed:
			return Response({'message': 'This email has been verified.'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			try:
				send_email_confirmation(request, user, email=email)
				return Response({'message': 'Confirmation message has been sent.'}, status=status.HTTP_200_OK)
			except APIException:
				return Response({'message': 'This email does not exist.'}, status=status.HTTP_403_FORBIDDEN)
"""
# from allauth.account.utils import complete_signup


class ResendEmailView(generics.CreateAPIView):
	""" This resends the email confirmation key to the user email. Parameter is only email"""
	serializer_class = ResendEmailSerializer
	permission_classes = [permissions.AllowAny]

	def create(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			# user = User.objects.get(email=request.data['email'])
			# email = user.emailaddress_set.get(email=request.data['email'])

			email = EmailAddress.objects.get(email=request.data['email'])
			user = email.user

			if not email.verified:
				send_email_confirmation(request, user, email=email)
				# complete_signup(self.request._request, user, all_auth_settings.EMAIL_VERIFICATION, None)
				return Response({'message': 'Confirmation message has been sent.'}, status=status.HTTP_200_OK)
			else:
				return Response({'message': 'This email has been verified.'}, status=status.HTTP_403_FORBIDDEN)
		else:
			return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
