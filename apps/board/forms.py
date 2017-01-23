from django import forms
from apps.board.models import Note


class NoteCreateForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ('title', 'content', )
