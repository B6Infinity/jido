from django.core.checks.messages import ERROR
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User

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
    logout(request)
    return redirect('home')

def handlelogin(request):
    if request.method == 'POST':
        RESPONSE = {"SUCCESS": True, "ERRORS": []}

        username = request.POST['login_username']
        password = request.POST['login_password']

        # Frisk Data
        if User.objects.filter(username=username).first() == None:
            RESPONSE['SUCCESS'] = False
            RESPONSE['ERROR'].append("Username does not exist!")

        
        # -------------- FINISH AFTER COMPLETING MESSAGES FRONT END ---------------
            

        # return redirect('home')