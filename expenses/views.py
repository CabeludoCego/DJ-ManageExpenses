from django.shortcuts import render

def index(request):
    return render(request, 'expenses/index.html');

def create(request):
    return render(request, 'expenses/create.html');