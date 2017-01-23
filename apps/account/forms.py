from django import forms
from django.utils.translation import ugettext as _
from django.core.validators import validate_email
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(
        max_length=25, widget=forms.PasswordInput())


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password', )
        widgets = {
            'password': forms.PasswordInput()
        }


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(max_length=255)

    def clean_email(self):
        email = self.data.get('email')
        validate_email(email)
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('invalid email address'))
        return email


class PasswordResetForm(forms.Form):
    password = forms.CharField(
        max_length=25, widget=forms.PasswordInput())
    password_reply = forms.CharField(
        max_length=25, widget=forms.PasswordInput())

    def clean_password(self):
        password = self.data.get('password')
        password_reply = self.data.get('password_reply')
        if password != password_reply:
            forms.ValidationError(_('password"s not matched'))
        return password
