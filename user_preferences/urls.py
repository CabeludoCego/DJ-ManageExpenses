from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt, csrf_protect

urlpatterns = [
	path('', views.index, name="preferences.index"),
	 
]