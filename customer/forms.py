from dataclasses import fields
from django.contrib.auth.models import User
from django import forms

from .models import *


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

class Mails(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = "__all__"
        

class ProfileEdit(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ['user']
        
class UserEdit(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", 'last_name', 'username', 'email']