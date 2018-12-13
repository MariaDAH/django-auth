from django.shortcuts import render,redirect,reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required  
from accounts.forms import UserFormLogin,UserRegistrationForm
from django.contrib.auth.models import User


# Create your views here.
"""Return index html"""
def index(request):
    return render(request,"index.html")
    
"""Logout user"""
@login_required
def logout(request):
    auth.logout(request)
    messages.info(request,"You have been succesfully logged out")
    return redirect(reverse('index'))
    
    
""""Login user"""
def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
        
    if request.method == "POST":
        login_form = UserFormLogin(request.POST)
        
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            messages.success(request,"Your are succesfully logged in!")
            
            if user:
                auth.login(user=user, request=request)
                return redirect(reverse('index'))
            else:
                login_form.add_error(None,"Your username and password are incorrect")
    else:
        login_form = UserFormLogin()
        #messages.info(request,"You have been logged in")
    return render(request,'login.html',{"login_form":login_form})
    
"""Register user"""
def registration(request):
    """Render the registration page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        
        if registration_form.is_valid():
            registration_form.save()
            
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
                                    
            if user:
                auth.login(user=user,request=request)
                messages.success(request,"You have successfully registered")
                #return redirect(reverse('index'))
            else:
                messages.error(request,"Unable to register your account at this time")
    else:
        registration_form = UserRegistrationForm()
    return render(request,'registration.html', {"registration_form": registration_form})
    
def user_profile(request):
    user = User.objects.get(email=request.user.email)
    return render(request,'profile.html')
    
