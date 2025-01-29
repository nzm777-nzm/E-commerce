from django import forms

from django.contrib.auth.forms import UserCreationForm

from myshoe.models import User,Order

class SignupForm(UserCreationForm):
    
    class Meta:
        
        model=User
        
        fields=["username","email","password1","password2","phone"]
        
        widgets={

            "username":forms.TextInput(attrs={'class':'form-control','placeholder':'username'}),
            "email":forms.EmailInput(attrs={'class':'form-control', 'placeholder':'email'}),
            "phone":forms.TextInput(attrs={'class':'form-control', 'placeholder':'phone'}),
            "password1":forms.TextInput(attrs={'class':'form-control', 'placeholder':'password1'}),
            "password2":forms.TextInput(attrs={'class':'form-control', 'placeholder':'password2'}),
            
        }
        

class LoginForm(forms.Form):
    

        username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), label='')
        password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), label='')
        
class OrderForm(forms.ModelForm):
    
    class Meta:
        
        model=Order
        
        fields=["address","phone","payment_method"]
    
    
        