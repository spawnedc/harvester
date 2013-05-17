from .models import User
from google.appengine.api import users
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class AutoCreateUser(object):

    def process_request(self, request):

        current_user = users.get_current_user()

        if current_user:
            user, created = User.objects.get_or_create(email=current_user.email())
            request.user = user
            request.user_is_admin = users.is_current_user_admin()

            if not request.path.startswith('/settings'):
                if not user.data_harvest_auth_key or not user.invoice_harvest_auth_key:
                    return HttpResponseRedirect(reverse('settings'))