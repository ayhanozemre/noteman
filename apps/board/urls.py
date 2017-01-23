from django.conf.urls import patterns, url
from apps.board import views

urlpatterns = patterns('',
    url(r'^$', views.NoteListView.as_view(), name='note-list'),
    url(r'^note-detail/(?P<pk>\d+)$', views.NoteDetailView.as_view(),
        name='note-detail'),
    url(r'^note-delete/(?P<pk>\d+)$', views.NoteDeleteView.as_view(),
        name='note-delete'),
    url(r'^note-create$', views.NoteCreateView.as_view(),
        name='note-create'),
)
