from django.contrib.auth.forms import UserCreationForm  
from django import forms
from django.contrib.auth.models import User
from .models import Profiles
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    phone=forms.CharField(max_length=10)

    class Meta:
        model=User
        fields=['username','email','phone','password1','password2']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Field('username', css_class='rounded-lg border-2 border-gray-300 p-2 w-full'),
            Field('email', css_class='rounded-lg border-2 border-gray-300 p-2 w-full'),
            Field('phone', css_class='rounded-lg border-2 border-gray-300 p-2 w-full'),
            Field('password1', css_class='rounded-lg border-2 border-gray-300 p-2 w-full'),
            Field('password2', css_class='rounded-lg border-2 border-gray-300 p-2 w-full'),
            Submit('submit', 'Sign Up', css_class='w-full bg-amber-500 hover:bg-amber-600 text-white py-2 rounded-full')
        )
    

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    phone=forms.CharField(max_length=10)

    class Meta:
        model=User
        fields=['username','email','phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        for field_name in self.fields:
            self.fields[field_name].help_text = None
            
            
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profiles
        fields = []
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_show_labels = True
            for field_name in self.fields:
                self.fields[field_name].help_text = None