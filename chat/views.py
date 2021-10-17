from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from chat.models import Chat, Message

# Create your views here.

# PAGEs
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


# APIs

def fetch_messages(request):
    if request.method == 'POST' and request.user.is_authenticated:

        chat_id = request.POST['chat_id']

        chat = Chat.objects.get(id=chat_id)
        if not request.user in chat.participants.all():
            return JsonResponse({"SUCCESS": False, "ERRORS": ['Critical Gateway!']})
        

        RESPONSE = {"SUCCESS": True, "ERRORS": []}

        messages = Message.objects.filter(chat=chat)

        RESPONSE['MESSAGES'] = {}

        for message in messages:
            RESPONSE['MESSAGES'][str(message.id)] = {
                "TEXT": message.message,
                "AUTHOR": message.author.username,
                "TIME_SENT": message.time_sent
            }
            


        return JsonResponse(RESPONSE)
