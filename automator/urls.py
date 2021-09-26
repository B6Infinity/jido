from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', view=views.home, name='home'),
    path('home', view=views.home, name='home'),
    path('login', view=views.loginorsignup, name='loginorsignup'),
    path('handlelogin', view=views.handlelogin, name='handlelogin'),
    path('logout', view=views.logoutuser, name='logoutuser'),
    path('myprofile', view=views.myprofile, name='myprofile'),
    path('handlesignup', view=views.handlesignup, name='handlesignup'),

    # APIs
    path('usernameexists', view=views.usernameexists, name='usernameexists'),

    # STATIC APIs


]