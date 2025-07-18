import re
from django.shortcuts import redirect, render
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views import View
import json
import pdb

from django.urls import reverse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from .utils import account_activation_token

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
            user.is_active = True
            user.save()
            
            uid64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link=reverse('activate', kwargs={
                'uid64': uid64, 'token': account_activation_token.make_token(user)})
            activate_url = 'http://'+ domain + link
            
            email_content = {
                'email_subject': 'Activate your account',
                'email_body': "Hello, " + user.username + ". Click on the link to activate your account and start using the app: \n" + activate_url + " .",
                'email_from': 'noreply@emycolon.com',
                'email_to': [email],
            }
            email = EmailMessage(
                email_content['email_subject'],
                email_content['email_body'],
                email_content['email_from'],
                email_content['email_to'],
            )
            # email.send(fail_silently=False)
            messages.success(request, "Account successfully created.")
        return render(request, 'authentication/register.html')
        
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                messages.success(request, 'Welcome, ' + user.username)  
                return redirect('expenses.index')
            elif not user:   
                messages.error(request, 'Invalid credentials, try again.')
            elif not user.is_active:
                messages.error(request, 'The account is not valid, check your email.')
            return render(request, 'authentication/login.html')   
        messages.error(request, 'Please fill all fields.')
        return render(request, 'authentication/login.html')   
                    

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You successfully logged out.')
        return redirect('login')

class UserVerificationView(View):
    def get(self, request, uid64, token):
        try:
            id = force_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=id)
            if not account_activation_token.check_token(user,token):
                return redirect('login' + '?message=' + 'User already activated.')
            if not user.is_active:
                user.is_active = True
                user.save()    
                messages.success(request, "Account activated successfully!")
            return redirect('login')
        
        except Exception as ex:
            pass    
        return redirect('login')
        
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