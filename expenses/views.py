from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from expenses.forms import ExpenseCreateModelForm
from .models import Expense, Category
from django.contrib.auth.models import User
from django.contrib import messages

@login_required(login_url="/auth/login")
def index(request):
    user = request.user
    expenses = Expense.objects.filter(owner = user)
    return render(request, 'expenses/index.html', {'expenses':expenses});

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
    