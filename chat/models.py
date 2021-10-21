from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name="chats")

    is_group_chat = models.BooleanField(default=False)
    title = models.CharField(max_length=150, blank=True)

    def save(self, *args, **kwargs):
        if len(self.participants.all()) > 2:
            self.is_group_chat = True
        else:
            self.is_group_chat = False
            

            
        if self.title.strip() == '' and self.is_group_chat:
            TITLE = f'Group Chat ({len(self.participants.all())})'
            
            self.title = TITLE


        super(Chat, self).save(*args, **kwargs)
    
        


    def __str__(self):
        s = ''
        for participant in self.participants.all():
            s += f'{participant.username} '

        return s

class Message(models.Model):
    message = models.TextField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='messages')

    time_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.message} ---[{self.author} > {self.chat}]'

