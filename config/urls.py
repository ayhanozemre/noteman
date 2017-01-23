from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^account/', include('apps.account.urls', namespace='account')),
    url(r'', include('apps.board.urls', namespace='board')),
    url(r'^admin/', include(admin.site.urls)),
)
