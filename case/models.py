from django.db import models
from django.conf import settings
import os
import shutil

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

    document = models.FileField(upload_to='temp/documents', null=True, blank=True)
    image = models.ImageField(upload_to='temp/images', null=True, blank=True)
    video = models.FileField(upload_to='temp/videos', null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # First save to get ID if it's new

        updated = False

        def move_file(field_name, upload_to_func):
            nonlocal updated
            file = getattr(self, field_name)
            if file and self.id:
                old_path = file.path
                new_relative_path = upload_to_func(self, os.path.basename(old_path))
                new_full_path = os.path.join(settings.MEDIA_ROOT, new_relative_path)

                if old_path != new_full_path:
                    os.makedirs(os.path.dirname(new_full_path), exist_ok=True)
                    shutil.move(old_path, new_full_path)
                    file.name = new_relative_path
                    updated = True

        move_file('document', upload_to_documents)
        move_file('image', upload_to_images)
        move_file('video', upload_to_videos)

        if updated:
            super().save(update_fields=['document', 'image', 'video'])

    def __str__(self):
        return self.title
