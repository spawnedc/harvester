from django.views.generic.base import View, TemplateView
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse_lazy

from .models import User
from .forms import UserSettingsForm
from .harvest import Harvest

import json

# Base views
class PublicBaseView(View):
    """ A base class for all views """

    class Meta:
        abstract = True

    def get_context_data(self, *args, **kwargs):
        context = super(PublicBaseView, self).get_context_data(*args, **kwargs)

        context['section'] = self.section_name or ''
        context['current_user'] = self.request.user
        context['user_is_admin'] = self.request.user_is_admin

        return context


class PublicBasicPageView(PublicBaseView, TemplateView):
    """ Basic page view """
    pass

# Page views
class HomeView(PublicBasicPageView):
    template_name = 'home.html'
    section_name = 'home'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        u = self.request.user
        h = Harvest(u.data_harvest_app_name, u.data_harvest_auth_key, u.data_harvest_user_id)
        context['report'] = h.get_report('20130420', '20130519')

        return context


home = HomeView.as_view()


class SettingsView(PublicBaseView, UpdateView):
    template_name = 'settings.html'
    section_name = 'settings'
    model = User
    form_class = UserSettingsForm
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user

settings = SettingsView.as_view()