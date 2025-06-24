from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views import View
import json
import pdb
from validate_email import validate_email
from django.contrib import messages

# Create your views here.

class RegisterView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # Get data
        username = request.POST['username'];
        email = request.POST['email'];
        password = request.POST['password'];
        context = {
            'fieldValues': request.POST
        }
        if (not User.objects.filter(username = username).exists()) and (not User.objects.filter(email = email).exists()):
            if len(password) < 6:
                messages.error(request, 'Password too short!')
                return render(request, 'authentication/register.html', context)
            user = User.objects.create_user(username, email, password)
            user.save()
            messages.success(request, "Account successfully created.")
        return render(request, 'authentication/register.html')
        

class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():     # is alphanumeric.
            return JsonResponse({
                'username_error': 'username should only contain alphanumeric characters.',
            }, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'username_error': "Username already exists or isn't valid.",
            }, status=409)
        return JsonResponse({'username_valid':True}, status=200)



class EmailValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):     # is alphanumeric.
            return JsonResponse({
                'email_error': 'Email is invalid.',
            }, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'email_error': "Email already has an account or isn't valid.",
            }, status=409)
        return JsonResponse({'email_valid':True}, status=200)