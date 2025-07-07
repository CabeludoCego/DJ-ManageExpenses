
from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="expenses.index"),
 	path('create/', views.create, name='expenses.create'),
 	path('create-form/', views.create_form, name='expenses.create-form'),
	path('update/<int:id>', views.update, name='expenses.update'),
 	path('archive/<int:id>', views.archive, name='expenses.archive'),
 	path('delete/<int:id>', views.delete, name='expenses.delete'),
 	
  
]
