# myapp/middleware.py

import uuid
import logging
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser


class GuestUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            guest_user_id = request.session.get('guest_user_id')
            if not guest_user_id:
                guest_user_id = str(uuid.uuid4())
                request.session['guest_user_id'] = guest_user_id
                request.user = AnonymousUser()
                request.user.guest_user_id = guest_user_id
                print(f"Created new guest_user_id: {guest_user_id}")
            else:
                request.user = AnonymousUser()
                request.user.guest_user_id = guest_user_id
                print(f"Retrieved existing guest_user_id: {guest_user_id}")
        else:
            print("User is authenticated")

    def process_response(self, request, response):
        if hasattr(request.user, 'guest_user_id'):
            response.set_cookie('guest_user_id', request.user.guest_user_id)
            print(f"Set guest_user_id cookie: {request.user.guest_user_id}")
        return response
