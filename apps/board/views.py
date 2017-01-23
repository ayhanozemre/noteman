from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from apps.board.models import Note
from apps.board.forms import NoteCreateForm


class NoteListView(ListView):
    model = Note
    template_name = 'board/note_list.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(NoteListView, self).get_context_data(*args, **kwargs)
        ctx['created_form'] = NoteCreateForm()
        return ctx


class NoteDetailView(DetailView):
    model = Note
    template_name = 'board/note_detail.html'

    def get_queryset(self):
        qs = super(NoteDetailView, self).get_queryset()
        return qs.filter(created_user=self.request.user)

    def get(self, request, *args, **kwargs):
        super(NoteDetailView, self).get(request, *args, **kwargs)
        return JsonResponse({
            'title': self.object.title,
            'content': self.object.content,
            'created_at': self.object.created_at})


class NoteDeleteView(NoteDetailView):

    def get(self, request, *args, **kwargs):
        super(NoteDeleteView, self).get(request, *args, **kwargs)
        self.object.delete()
        return redirect(reverse('board:note-list'))


class NoteCreateView(View):
    model = Note
    form_class = NoteCreateForm

    def create(self, **kwargs):
        return self.model.object.get_or_create(**kwargs)

    def post(self, request, *args, **kwargs):
        form = NoteCreateForm(request.POST)
        form.instance.created_user = self.request.user
        form.save()
        return redirect(reverse('board:note-list'))
