from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import User
from django.db.models import ForeignKey

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to='profile_pics', blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title} by {self.author.username}"
