from django.db import models
from django.conf import settings

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

    # File handling (can store PDFs, DOCs, images, and videos)
    document = models.FileField(upload_to='documents/', null=True, blank=True)  # for general documents (PDF, DOC)
    image = models.ImageField(upload_to='images/', null=True, blank=True)  # for images (e.g., JPG, PNG)
    video = models.FileField(upload_to='videos/', null=True, blank=True)  # for videos (e.g., MP4, AVI)

    def __str__(self):
        return self.title
