from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import build_absolute_uri
from django.conf import settings 

class CustomAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        url =f'{settings.FRONTEND_URL}/{emailconfirmation.key}/'
        ret = build_absolute_uri(request, url)
        return ret