
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt, csrf_protect

urlpatterns = [
	path('register', views.RegisterView.as_view(), name="register"),
	# path('validate-username', views.UsernameValidationView(), name="validate-username"),
 	path('validate-username', csrf_exempt(views.UsernameValidationView.as_view())),
	path('validate-email', csrf_exempt(views.EmailValidationView.as_view())),
	
	
 
]