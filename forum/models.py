from django.db import models
from django.contrib.auth.models import User

class ForumPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    bookmark = models.BooleanField(default=False)
    isDraft = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    editHistory = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title

class ForumComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    editHistory = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Comment by {self.author} on Post {self.post.id}"

class ForumReply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    comment = models.ForeignKey(ForumComment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    editHistory = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Reply by {self.author} on Comment {self.comment.id}"
