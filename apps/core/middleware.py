from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile


EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:

    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware\
        requires authentication middleware to be installed. Edit your\
        MIDDLEWARE_CLASSES setting to insert\
        'django.contrib.auth.middleware.AuthenticationMiddleware'. \
        If that doesn't work, ensure your \
        TEMPLATE_CONTEXT_PROCESSORS setting includes\
        'django.core.context_processors.auth'."
        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)
