from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # Pages
    path('', view=views.home, name='home'),

    # APIs
    path('fetch_messages', view=views.fetch_messages, name='fetch_messages'),
]