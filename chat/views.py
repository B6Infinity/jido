from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from chat.models import Chat, Message

# Create your views here.


def home(request):
    if request.user.is_authenticated:


        # for chat in Chat.objects.filter(recipient=request.user):
        #     print(chat)


        RESPONSE = {
            "CHATS": request.user.chats.all()
        }

        return render(request, 'chat/home.html', RESPONSE)
    else:
        return redirect('/login')
    