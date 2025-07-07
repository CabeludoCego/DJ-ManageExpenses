from operator import is_
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from expenses.forms import ExpenseCreateModelForm
from .models import Expense, Category
from django.contrib.auth.models import User
from django.contrib import messages

@login_required(login_url="/auth/login")
def index(request):
    user = request.user
    expenses = Expense.objects.filter(owner = user, is_active=True)
    categories = Category.objects.all()
    context = {
        'expenses':expenses,
        'categories': categories
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