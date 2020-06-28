from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo
from django.core import validators


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    verify_email = forms.EmailField(label='Enter your email again:')

    def clean(self):
        all_clean_data = super().clean()
        email = all_clean_data['email']
        vmail = all_clean_data['verify_email']

        if email != vmail:
            raise forms.ValidationError('MAKE SURE EMAILS MATCH')

    class Meta():
        model = User
        fields = ('username', 'email', 'verify_email', 'password')


class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
