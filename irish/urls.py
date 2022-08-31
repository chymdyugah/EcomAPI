from django.conf.urls import url, include
from . import views
from dj_rest_auth.registration.views import ConfirmEmailView
from dj_rest_auth.views import ResendEmailView

app_name = "irish"

urlpatterns = [
	url(r'^$', views.Index.as_view(), name='index'),
	url(r'^shop/$', views.Shop.as_view(), name='shop'),
	# url(r'^shop/(?P<category>[a-z]+)/$', views.Category.as_view(), name='category'),
	url(r'^cart/$', views.CartView.as_view(), name='cart'),
	url(r'^single/(?P<prodid>[a-z0-9]+)/$', views.Single.as_view(), name='single'),
	url(r'^users/', include('dj_rest_auth.urls')),
	url(r'^users/registration/', include('dj_rest_auth.registration.urls')),
	url(r'^users/registration/confirm-email/<str:key>/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
	url(r'users/google/login/$', views.GoogleLogin.as_view(), name='google_login'),
	url(r'users/facebook/login/$', views.FacebookLogin.as_view(), name='facebook_login'),
	url(r'users/resend-email-verification/$', ResendEmailView.as_view(), name='resend_email_confirm'),
]
