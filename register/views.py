from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm  
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profiles
from .forms import UserRegistrationForm,ProfileUpdateForm,UserUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(requests):
    if requests.method=="POST":
        form=UserRegistrationForm(requests.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(requests,f"Account has been successfully created for {username}") 
            return redirect('foodcateringweb.home')
    else:
        form=UserRegistrationForm()
    
    return render(requests,'register/register.html',{'form':form})

def logout_view(request):
    logout(request)
    return render(request, 'register/logout.html')

@login_required
def profile(request):
    if request.method=="POST":
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profiles)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Your Account has been updated successfully!!')
            return redirect('foodcateringweb.home')
    else:
        
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profiles)
    forms={
        'u_form':u_form,
        'p_form':p_form
    }
    
        
    return render(request,'register/profile.html',forms)