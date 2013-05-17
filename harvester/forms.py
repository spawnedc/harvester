from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

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
    class Meta:
        model = User
        fields = ('data_harvest_auth_key', 'invoice_harvest_auth_key',)

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)
        self.helper.form_action = 'settings/'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.set_field_classes('span5')