from django.db import models
from django.conf import settings
import os

def upload_to_documents(instance, filename):
    return os.path.join('documents', f'case_{instance.id}', filename)

def upload_to_images(instance, filename):
    return os.path.join('images', f'case_{instance.id}', filename)

def upload_to_videos(instance, filename):
    return os.path.join('videos', f'case_{instance.id}', filename)

class Case(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('ongoing', 'Ongoing'),
        ('discarded', 'Discarded'),
        ('closed', 'Closed'),
    ]

    TYPE_CHOICES = [
        ('family', 'Family Law'),
        ('criminal', 'Criminal Law'),
        ('civil', 'Civil Law'),
        ('labor', 'Labor Law'),
        ('commercial', 'Commercial and Business Law'),
        ('other', 'Others'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cases")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    case_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='criminal')
    created_date = models.DateTimeField(auto_now_add=True)

    document = models.FileField(upload_to=upload_to_documents, null=True, blank=True)
    image = models.ImageField(upload_to=upload_to_images, null=True, blank=True)
    video = models.FileField(upload_to=upload_to_videos, null=True, blank=True)

    def __str__(self):
        return self.title
