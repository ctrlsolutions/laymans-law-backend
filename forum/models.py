from django.db import models
from django.conf import settings


class ForumPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum')
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    bookmark = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
