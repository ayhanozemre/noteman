from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    created_user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.title)
