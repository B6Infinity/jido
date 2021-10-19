from django.db import models
from django.contrib.auth.models import User
import json

# VARs

PROGRAMMING_LANGUAGES = []

OS_PLATFORMS = []

# Import The Variables from the files into VARs
with open('automator/PROGRAMMING_LANGUAGES.json', 'r') as f:
    programming_languages = json.load(f)
with open('automator/OS_PLATFORMS.json', 'r') as f:
    os_platforms = json.load(f)

for language in programming_languages:
    PROGRAMMING_LANGUAGES.append((language, programming_languages[language]))

for platform in os_platforms:
    OS_PLATFORMS.append((platform, os_platforms[platform]))





# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserProfile')
    github_username = models.CharField(max_length=39, null=True, blank=True)
    is_developer = models.BooleanField(default=False)

    profilePic_url = models.TextField(default="https://rpgplanner.com/wp-content/uploads/2020/06/no-photo-available.png", blank=True)

    online = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if self.github_username is not None:
            if len(self.github_username.strip()) != 0: # User has a GitHub Username
                self.profilePic_url = f'https://avatars.githubusercontent.com/{self.github_username}'
                self.is_developer = True
            else:
                self.profilePic_url = f'https://rpgplanner.com/wp-content/uploads/2020/06/no-photo-available.png'
                self.is_developer = False

        else:
            self.profilePic_url = f'https://rpgplanner.com/wp-content/uploads/2020/06/no-photo-available.png'
            self.is_developer = False


        super(UserProfile, self).save(*args, **kwargs)
    
    


    def __str__(self) -> str:
        return str(self.user) + f" - {self.github_username}"


class Command(models.Model):
    command_string = models.CharField(max_length=90)
    def __str__(self) -> str:
        return self.command_string

class Automation(models.Model):

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    brief_explanation = models.TextField(max_length=150, null=False)
    programming_language = models.CharField(max_length=90, choices=PROGRAMMING_LANGUAGES, default='None')

    platform = models.CharField(max_length=90, choices=OS_PLATFORMS, default='None')

    github_repo_URL = models.CharField(max_length=170)

    readme = models.TextField(default="", blank=True)

    commands = models.ManyToManyField(Command, related_name="automation")

    def __str__(self) -> str:
        return f"{self.author.username} - {self.brief_explanation}"


    