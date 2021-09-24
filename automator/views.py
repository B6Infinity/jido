from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout, login

# Create your views here.
def home(request):
    return render(request, 'home.html')

def loginorsignup(request):
    if request.user.is_authenticated:
        return redirect('myprofile')

    return render(request, 'login.html')

def myprofile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'userprofile.html')

def logoutuser(request):
    logout(request.user)
    return redirect('home')