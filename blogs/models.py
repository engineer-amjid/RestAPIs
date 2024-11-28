from django.db import models
from django.contrib.auth.models import User
from django.db.models import ForeignKey


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title} by {self.author.username}"