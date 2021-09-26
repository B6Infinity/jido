from automator.models import UserProfile
from django.core.checks.messages import ERROR
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib import messages

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
        # RESPONSE = {"SUCCESS": True, "ERRORS": []}

        username = request.POST['login_username']
        password = request.POST['login_password']

        # Frisk Data
        if User.objects.filter(username=username).first() == None:
            # RESPONSE['SUCCESS'] = False
            # RESPONSE['ERROR'].append("Username does not exist!")
            messages.error(request, "Username does not exist!")
            
            return redirect('loginorsignup')
        
        login_user = authenticate(username=username, password=password)

        if login_user is None:
            messages.error(request, "Invalid Passsword!")
            return redirect('loginorsignup')
        
        # Correct Creds - Login Now... HAYAKU!

        messages.success(request, f"Logged in as {login_user}!")

        login(request, login_user)

        return redirect('home')
       
def handlesignup(request):
    if request.method == 'POST':
        # RESPONSE = {"SUCCESS": True, "ERRORS": []}

        signup_username = request.POST['signup_username']
        first_name = request.POST['first_name']
        email = request.POST['email']
        github_username = request.POST['github_username']
        signup_password = request.POST['signup_password']
        cf_signup_password = request.POST['cf_signup_password']
        agreed2TNC = request.POST['agreed2TNC']


        # Frisk Data

        ERROR_COUNT = 0

        if User.objects.filter(username=signup_username).first() != None:
            ERROR_COUNT += 1
            messages.error(request, "Username already exists!")
        
        if signup_password != cf_signup_password:
            ERROR_COUNT += 1
            messages.error(request, "Passwords don't match!")

        if agreed2TNC != 'on':
            ERROR_COUNT += 1
            messages.error(request, "You must agree to the <a href='#'>Terms and Conditions</a>")

        if ERROR_COUNT != 0:
            return redirect('signuporlogin')

        # CREATE USER NOW

        newuser = User.objects.create(username=signup_username, password=signup_password, first_name=first_name, email=email)
        UserProfile.objects.create(user=newuser,github_username=github_username)

        messages.success(request, f"Logged in as {newuser}")
        login(request, newuser)

        return redirect('home')


# APIs

def usernameexists(request):
    if request.method == 'POST':
        RESPONSE = {"SUCCESS": True, "ERRORS": []}

        username_to_check_availability = request.POST['username_to_check_availability']

        if User.objects.filter(username=username_to_check_availability).first()!= None:
            RESPONSE['SUCCESS'] = False
            RESPONSE['ERRORS'].append("Username Already Exists")

        return JsonResponse(RESPONSE)
        


