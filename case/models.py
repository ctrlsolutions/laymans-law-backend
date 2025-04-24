from django.db import models
from django.conf import settings
import os

def upload_to_documents(instance, filename):
    # Ensure that the instance is saved and the user is populated
    if instance.created_by and instance.created_by.user_id:  # Use user_id instead of id
        return os.path.join('documents', f'user_{instance.created_by.user_id}', f'case_{instance.id}', filename)
    return os.path.join('documents', 'default', filename)

def upload_to_images(instance, filename):
    if instance.created_by and instance.created_by.user_id:  # Use user_id instead of id
        return os.path.join('images', f'user_{instance.created_by.user_id}', f'case_{instance.id}', filename)
    return os.path.join('images', 'default', filename)

def upload_to_videos(instance, filename):
    if instance.created_by and instance.created_by.user_id:  # Use user_id instead of id
        return os.path.join('videos', f'user_{instance.created_by.user_id}', f'case_{instance.id}', filename)
    return os.path.join('videos', 'default', filename)


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

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Save to generate ID

        if is_new:
            # Debugging: Check the CustomUser object
            if self.created_by:
                print(f"Created By (User): {self.created_by} | user_id: {getattr(self.created_by, 'user_id', None)}")
            
            if self.document:
                self.document.name = upload_to_documents(self, os.path.basename(self.document.name))
            if self.image:
                self.image.name = upload_to_images(self, os.path.basename(self.image.name))
            if self.video:
                self.video.name = upload_to_videos(self, os.path.basename(self.video.name))

            # Save again after setting the correct paths
            super().save(update_fields=['document', 'image', 'video'])
