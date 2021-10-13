from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', view=views.home, name='home'),
    path('home', view=views.home, name='home'),

    # Authentication and Stuff
    path('login', view=views.loginorsignup, name='loginorsignup'),
    path('handlelogin', view=views.handlelogin, name='handlelogin'),
    path('logout', view=views.logoutuser, name='logoutuser'),
    path('myprofile', view=views.myprofile, name='myprofile'),
    path('handlesignup', view=views.handlesignup, name='handlesignup'),
    path('updateusertodev', view=views.updateusertodev, name='updateusertodev'),

    # Applicative
    path('automationcreator', view=views.automationcreator, name='automationcreator'),
    path('createautomation', view=views.createautomation, name='createautomation'),



    # APIs
    path('usernameexists', view=views.usernameexists, name='usernameexists'),
    path('gh_usernameexists', view=views.gh_usernameexists, name='gh_usernameexists'),

    # STATIC APIs


]