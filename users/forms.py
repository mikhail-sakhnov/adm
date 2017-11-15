from django.forms import ModelForm, Form, CharField
from users.models import AdmUser


class AdmUserForm(ModelForm):

    class Meta:
        model = AdmUser
        fields = ['full_name', 'full_address', 'email']


class SubmitForm(Form):
    token = CharField(label='Token', max_length=100)


class ControlForm(Form):
    mode = CharField(label="mode", max_length=100)
