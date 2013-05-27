from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .harvest import Harvest

import base64

class HarvesterBaseModelForm(forms.ModelForm):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.html5_required = True

        super(HarvesterBaseModelForm, self).__init__(*args, **kwargs)


    def set_field_classes(self, css_class):
        """ Sets class of all the fields to the given class name """

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = css_class

class UserSettingsForm(HarvesterBaseModelForm):
    data_harvest_email = forms.CharField(max_length=200)
    data_harvest_password = forms.CharField(max_length=200, widget=forms.PasswordInput)
    invoice_harvest_email = forms.CharField(max_length=200)
    invoice_harvest_password = forms.CharField(max_length=200, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('data_harvest_app_name', 'data_harvest_email', 'data_harvest_password', 'invoice_harvest_app_name', 'invoice_harvest_email', 'invoice_harvest_password',)

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))
        self.set_field_classes('span5')

    def clean(self):
        cleaned_data = super(UserSettingsForm, self).clean()

        data_harvest_auth_key = '%s:%s' % (cleaned_data['data_harvest_email'], cleaned_data['data_harvest_password'])
        invoice_harvest_auth_key = '%s:%s' % (cleaned_data['invoice_harvest_email'], cleaned_data['invoice_harvest_password'])

        cleaned_data['data_harvest_auth_key'] = base64.encodestring(data_harvest_auth_key).replace('\n','')
        cleaned_data['invoice_harvest_auth_key'] = base64.encodestring(invoice_harvest_auth_key).replace('\n','')

        return cleaned_data

    def save(self, *args, **kwargs):
        user = super(UserSettingsForm, self).save(*args, **kwargs)
        user.data_harvest_auth_key = self.cleaned_data.get('data_harvest_auth_key')
        user.invoice_harvest_auth_key = self.cleaned_data.get('invoice_harvest_auth_key')

        h_data = Harvest(user.data_harvest_app_name, user.data_harvest_auth_key)
        user.data_harvest_user_id = int(h_data.user_data.get('user').get('id'))

        h_invoice = Harvest(user.invoice_harvest_app_name, user.invoice_harvest_auth_key)
        user.invoice_harvest_user_id = int(h_invoice.user_data.get('user').get('id'))

        user.save()
        return user
