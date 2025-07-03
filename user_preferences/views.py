from django import urls
from django.shortcuts import render
import os, json
from django.views import View
from django.conf import settings
from django.contrib import messages
from .models import UserPreferences

class Index(View):
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path) as data_file:
        data_loaded = json.load(data_file)
        currency_list = []
        for key, value in data_loaded.items():
            currency_list.append({"key": key, "value": value})
    
    def get(self, request):    
        user_preferences = UserPreferences.objects.filter(user=request.user)[ 0] if UserPreferences.objects.filter(user=request.user).exists() else None
        return render(request, 'preferences/index.html', {'currency_list': self.currency_list, 'preferences': user_preferences})
    
    def post(self,request):
        # import pdb; pdb.set_trace()
        user_exists = UserPreferences.objects.filter(user=request.user).exists()
        user_preferences = None
        currency = request.POST['currency']
        
        if user_exists:
            user_preferences = UserPreferences.objects.get(user=request.user)
            user_preferences.currency = currency
            user_preferences.save()
        else:
            UserPreferences.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved!')
        return render(request, 'preferences/index.html', {'currency_list': self.currency_list, 'preferences': user_preferences})
        

# Create your views here.
# def index(request):
#     file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    
#     with open(file_path) as data_file:
#         data_loaded = json.load(data_file)
#         # for k, v in data_loaded.items():
#         #   currency_data.append({'name': k, 'value': v})

#     currency_list = data_loaded
#     # import pdb;;
#     # pdb.set_trace()
#     # currency_list = []
#     return render(request, 'preferences/index.html', {'currency_list': currency_list})
