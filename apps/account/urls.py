from django.conf.urls import patterns, url
from apps.account import views


urlpatterns = patterns('',
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^register$', views.RegisterView.as_view(), name='register'),
    url(r'^password-reset/(?P<token>.+)$', views.PasswordResetView.as_view(),
        name='password-reset'),
    url(r'^forgot-password$', views.ForgotPasswordView.as_view(),
        name='forgot-password'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
)
