from django import forms
from django.core.exceptions import ValidationError
from password_reset_email.models import PasswordResetEmail
from EmailUser.models import MyUser

class ResetPasswordForm(forms.Form):
    key = forms.CharField(
        max_length=100,
        required=True,
    )

    password1 = forms.CharField(
        max_length=100,
        required=True,
        widget = forms.PasswordInput()
    )

    password2 = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput()
    )


class RequestKeyForm(forms.Form):

    email = forms.EmailField(
        required=True
    )

