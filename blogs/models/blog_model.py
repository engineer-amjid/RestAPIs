from django.contrib.auth.models import User
from django.db import models
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author.username}"
