
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt, csrf_protect

urlpatterns = [
	path('register', views.RegisterView.as_view(), name="register"),
	path('login', views.LoginView.as_view(), name="login"),
	path('logout', views.LogoutView.as_view(), name="logout"),
	# path('validate-username', views.UsernameValidationView(), name="validate-username"),
 	path('validate-username', csrf_exempt(views.UsernameValidationView.as_view())),
	path('validate-email', csrf_exempt(views.EmailValidationView.as_view())),
	path('activate/<uid64>/<token>', views.UserVerificationView.as_view(), name='activate'),
 	
 
]