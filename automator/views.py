from automator.models import UserProfile
from django.core.checks.messages import ERROR
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests

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
        
        # Check the GitHub Username
        if len(github_username.strip()) != 0:
            url = f'https://api.github.com/users/{github_username}'
            response_from_githubAPI = requests.get(url=url).json()
            if 'message' in response_from_githubAPI:
                if response_from_githubAPI["message"] == 'Not Found':
                    ERROR_COUNT += 1
                    messages.error(request, "GitHub Username does not exist!")
            elif 'login' not in response_from_githubAPI:
                ERROR_COUNT += 1
                messages.error(request, "GitHub Username does not exist!")

            


        if ERROR_COUNT != 0:
            return redirect('loginorsignup')

        # CREATE USER NOW

        newuser = User.objects.create_user(username=signup_username, password=signup_password, first_name=first_name, email=email)
        UserProfile.objects.create(user=newuser,github_username=github_username)

        messages.success(request, f"Logged in as {newuser}")
        login(request, newuser)

        return redirect('home')

def updateusertodev(request):
    if not request.user.is_authenticated:
        return redirect('login')

    
    if request.method == 'POST':
        # RESPONSE = {"SUCCESS": True, "ERRORS": []}

        gh_username = request.POST['github_username']

        # Frisk The Availability
        if UserProfile.objects.filter(github_username=gh_username).first() != None:
            messages.error("GitHub Username Already in Use!")
            return redirect('automationcreator')

        profile = UserProfile.objects.get(user=request.user)
        profile.github_username = gh_username
        profile.save()

        return redirect('automationcreator')
        
    
    

# Applicative
def automationcreator(request):
    if request.user.is_authenticated:
        PARAMETERS = {"USER_IS_DEV": UserProfile.objects.get(user=request.user).is_developer}
    else:
        messages.info(request, "You need to login first!")
        return redirect('loginorsignup')

    

    return render(request, 'automation_creator.html', PARAMETERS)


# APIs

def usernameexists(request):
    if request.method == 'POST':
        RESPONSE = {"SUCCESS": True, "ERRORS": []}

        username_to_check_availability = request.POST['username_to_check_availability']

        if User.objects.filter(username=username_to_check_availability).first()!= None:
            RESPONSE['SUCCESS'] = False
            RESPONSE['ERRORS'].append("Username Already Exists")

        return JsonResponse(RESPONSE)
        
def gh_usernameexists(request):
    if request.method == 'POST':
        RESPONSE = {"SUCCESS": True, "ERRORS": []}

        gh_username_to_check_availability = request.POST['gh_username']

        if UserProfile.objects.filter(github_username=gh_username_to_check_availability).first() != None:
            RESPONSE['SUCCESS'] = False
            RESPONSE['ERRORS'].append("GitHub Username Already in Use!")

        return JsonResponse(RESPONSE)

