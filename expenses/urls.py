
from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="expenses.index"),
 	path('create/', views.create, name='expenses.create')
]
