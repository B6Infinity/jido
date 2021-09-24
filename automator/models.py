from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    github_username = models.CharField(max_length=39, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user) + f" - {self.github_username}"
