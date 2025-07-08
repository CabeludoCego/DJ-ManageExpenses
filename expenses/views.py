from operator import is_
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from expenses.forms import ExpenseCreateModelForm
from .models import Expense, Category
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
import json

# @login_required(login_url="/auth/login")
# def search_expenses(request):
#     if request.method == 'POST':
#         search_str = json.loads(request.body).get('searchText')
#         expenses = Expense.filter(amount__starts_with=search_str, owner=request.user) | Expense.filter(date__starts_with=search_str, owner=request.user) | Expense.filter(description__icontains=search_str, owner=request.user) | Expense.filter(category__icontains=search_str, owner=request.user)
    
#         data = expenses.values()
#         return JsonResponse(list(data), safe = False)
        
@login_required(login_url="/auth/login")
def index(request):
    user = request.user
    expenses = Expense.objects.filter(owner = user, is_active=True)
    categories = Category.objects.all()
    paginator = Paginator(expenses,10)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'expenses':expenses,
        'categories': categories,
        'page_obj': page_obj
    }
    return render(request, 'expenses/index.html', context);

@login_required(login_url="/auth/login")
def create(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    if request.method == 'GET':
        return render(request, 'expenses/create.html', context);
    elif request.method == 'POST':
        context['values'] = request.POST
        amount = request.POST['amount'] 
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']
        
        expense = Expense.objects.create(
        amount=amount, description=description, date=date, category=category, owner=request.user)
        if expense:
            messages.success(request,  'Expense was submitted successfully')        
            return redirect('expenses.index')
        return render(request, 'expenses/create.html', context);
        
@login_required(login_url="/auth/login")
def create_form(request):
    if request.method == 'POST':
        form = ExpenseCreateModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses.index')
        else:
            messages.error(request, 'Form is invalid!')
    else:
        form = ExpenseCreateModelForm()
    return render(request, 'expenses/create-djForm.html', {'form': form})

@login_required(login_url="/auth/login")
def update(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'categories': categories,
    }
    if request.method == 'GET':
        return render(request, 'expenses/update.html', context);
    if request.method == 'POST':
        amount = request.POST['amount'] 
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']
        
        # METHOD 1: ONE by one
        # expense.amount = amount
        # expense.date = date
        # expense.category = category
        # expense.description = description
        # expense.save()
        
        # METHOD 2: Update or create method
        Expense.objects.update_or_create( pk=id, defaults={
            "amount": amount,"description": description, "date":date, "category":category})
        messages.success(request, 'Expense updated successfully!')
        
        return redirect('expenses.index')
    

@login_required(login_url="/auth/login")
def archive(request, id):    
    expense = Expense.objects.get(pk=id)
    expense.is_active = False
    expense.save()
    messages.success(request, 'Expense archived!')
    return redirect('expenses.index')
    
    
@login_required(login_url="/auth/login")
def delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense removed!")
    return redirect('expenses.index')

        

# @login_required(login_url="/auth/login")
# def update_form(request, id):
#     expense = Expense.objects.get(pk=id)
#     categories = Category.objects.all()
#     context = {
#         'expense': expense,
#         'categories': categories,
#     }
#     # import pdb; pdb.set_trace()
#     if request.method == 'GET':
#         return render(request, 'expenses/update.html', context);
#     if request.method == 'POST':
#         amount = request.POST['amount'] 
#         description = request.POST['description']
#         category = request.POST['category']
#         date = request.POST['date']
        
#         Expense.objects.update_or_create( pk=id, defaults={
#             "amount": amount,"description": description, "date":date, "category":category})
#         messages.success(request, 'Expense updated successfully!')
        
#         return redirect('expenses.index')