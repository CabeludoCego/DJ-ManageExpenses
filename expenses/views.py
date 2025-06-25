from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="/auth/login")
def index(request):
    return render(request, 'expenses/index.html');

@login_required(login_url="/auth/login")
def create(request):
    return render(request, 'expenses/create.html');