from django import template
from ..models import UserProfile

register = template.Library()


@register.filter
def getProfilePictureURL(user):
    profilepicURL = UserProfile.objects.get(user=user).profilePic_url

    return profilepicURL

@register.filter
def getGitHubURL(user):
    ghusername = UserProfile.objects.get(user=user).github_username

    return f'https://github.com/{ghusername}/'
