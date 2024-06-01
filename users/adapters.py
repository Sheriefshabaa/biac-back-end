# myapp/adapters.py

from allauth.account.adapter import DefaultAccountAdapter
from .models import CustomUser
class CustomAccountAdapter(DefaultAccountAdapter):

    def confirm_email(self, request, email_address):
        email_address.verified = True
        email_address.save()

        
        user = CustomUser.objects.get(email=email_address.email)
        user.is_active = True
        user.save()

        return user
