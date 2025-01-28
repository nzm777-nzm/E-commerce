from django import forms

from django.contrib.auth.forms import UserCreationForm

from myshoe.models import User,Order

class SignupForm(UserCreationForm):
    
    class Meta:
        
        model=User
        
        fields=["username","email","password1","password2","phone"]
        

class LoginForm(forms.Form):
    

        username=forms.CharField()
        
        password=forms.CharField()
        
class OrderForm(forms.ModelForm):
    
    class Meta:
        
        model=Order
        
        fields=["address","phone","payment_method"]
    
    
        