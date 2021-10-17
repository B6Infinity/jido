from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # Pages
    path('', view=views.home, name='home'),
    path('home', view=views.home, name='home'),
    path('login', view=views.loginorsignup, name='loginorsignup'),
    path('myprofile', view=views.myprofile, name='myprofile'),
    path('viewprofile-<str:username>', view=views.viewprofile, name='viewprofile'),
    path('viewautomation-<str:automationid>', view=views.viewautomation, name='viewautomation'),

    # Authentication and Stuff
    path('handlelogin', view=views.handlelogin, name='handlelogin'),
    path('logout', view=views.logoutuser, name='logoutuser'),
    path('handlesignup', view=views.handlesignup, name='handlesignup'),
    path('updateusertodev', view=views.updateusertodev, name='updateusertodev'),

    # Applicative
    path('automationcreator', view=views.automationcreator, name='automationcreator'),
    path('createautomation', view=views.createautomation, name='createautomation'),


    # APIs
    path('usernameexists', view=views.usernameexists, name='usernameexists'),
    path('gh_usernameexists', view=views.gh_usernameexists, name='gh_usernameexists'),

    # STATIC APIs
    path('username_profilepic-<str:username>', view=views.get_username_profilepic, name='get_username_profilepic'),


]