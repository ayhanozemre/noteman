from django.views.generic import FormView, RedirectView, CreateView
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from apps.account.structure import EmailSenderTuple
from apps.account.forms import (LoginForm, RegisterForm,
                                ForgotPasswordForm, PasswordResetForm)
from apps.core.utils import send_email, redis_auth_db


class LoginView(FormView):
    template_name = 'account/login.html'
    form_class = LoginForm

    @property
    def success_url(self):
        return reverse('board:note-list')

    def get_user_payload(self):
        return (self.request.POST.get('username'),
                self.request.POST.get('password'))

    def form_valid(self, form):
        redirect_obj = super(LoginView, self).form_valid(form)
        username, password = self.get_user_payload()
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(self.request, user)
            return redirect_obj
        else:
            form.errors['__all__'] = _('invalid username or password!')
            return self.form_invalid(form)
        return redirect_obj


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'account/register.html'

    @property
    def success_url(self):
        return reverse('account:login')

    def form_valid(self, form):
        redirect_obj = super(RegisterView, self).form_valid(form)
        self.object.set_password(self.request.POST.get('password'))
        self.object.save()
        return redirect_obj


class ForgotPasswordView(FormView):
    template_name = 'account/forgot_password.html'
    form_class = ForgotPasswordForm

    @property
    def success_url(self):
        return reverse('account:login')

    def get_email_sender_payload(self):
        return EmailSenderTuple(
            subject=_('Forgot Password Email'),
            content_template='account/email/forgot_password.html',
            from_email=settings.EMAIL_HOST_USER,
            recipient_tuple=(self.request.POST.get('email'), ),
            http_host=self.request.META['HTTP_HOST'],
            http_schema=self.request.META['wsgi.url_scheme'])

    def form_valid(self, form):
        redirect_obj = super(ForgotPasswordView, self).form_valid(form)
        messages.success(
            self.request, _('You can reset password check your email'))
        send_email(self.get_email_sender_payload())
        return redirect_obj


class PasswordResetView(FormView):
    template_name = 'account/password_reset.html'
    form_class = PasswordResetForm

    def dispatch(self, *args, **kwargs):
        self.email = self.get_user_email()
        if not User.objects.filter(email=self.email).exists():
            messages.error(self.request, _('Invalid token'))
            return redirect(reverse('account:login'))
        return super(PasswordResetView, self).dispatch(*args, **kwargs)

    @property
    def success_url(self):
        return reverse('account:login')

    def get_user_email(self):
        return redis_auth_db.get(self.kwargs.get('token'))

    def form_valid(self, form):
        redirect_obj = super(PasswordResetView, self).form_valid(form)
        user = User.objects.get(email=self.email)
        user.set_password(self.request.POST.get('password'))
        user.save()
        messages.success(self.request, _('Password Changed!'))
        return redirect_obj


class LogoutView(RedirectView):

    @property
    def url(self):
        return reverse('account:login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
