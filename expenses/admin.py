from django.contrib import admin
from .models import Expense, Category

# Register your models here.

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
	list_display = ('id', 'amount', 'date', 'description', 'owner', 'category', 'is_active') 
	list_filter = ['owner', 'date', 'category'] 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id','name')
	list_filter = ['name']
