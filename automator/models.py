from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserProfile')
    github_username = models.CharField(max_length=39, null=True, blank=True)
    is_developer = models.BooleanField(default=False)

    profilePic_url = models.TextField(default="https://rpgplanner.com/wp-content/uploads/2020/06/no-photo-available.png", blank=True)



    def save(self, *args, **kwargs):

        if len(self.github_username.strip()) != 0: # User has a GitHub Username
            self.profilePic_url = f'https://avatars.githubusercontent.com/{self.github_username}'
            self.is_developer = True


        super(UserProfile, self).save(*args, **kwargs)
    
    


    def __str__(self) -> str:
        return str(self.user) + f" - {self.github_username}"
