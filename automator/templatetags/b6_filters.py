from django import template
from ..models import UserProfile

register = template.Library()

@register.filter
def passer():
    pass

@register.filter
def getProfilePictureURL(user):
    profilepicURL = UserProfile.objects.get(user=user).profilePic_url

    return profilepicURL

