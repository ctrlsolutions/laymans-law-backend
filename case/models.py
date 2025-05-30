from django.db import models
from django.conf import settings
import os

def upload_to_documents(instance, filename):
    if instance.created_by and instance.created_by.user_id:
        return os.path.join('documents', f'user_{instance.created_by.user_id}', f'case_{instance.id}', filename)
    return os.path.join('documents', 'default', filename)

def upload_to_images(instance, filename):
    if instance.created_by and instance.created_by.user_id:
        case_id = instance.id if instance.id else 'temp'
        path = os.path.join('images', f'user_{instance.created_by.user_id}', f'case_{case_id}')
        
        full_path = os.path.join(settings.MEDIA_ROOT, path)
        os.makedirs(full_path, exist_ok=True)

        return os.path.join(path, filename)
    return os.path.join('images', 'default', filename)

def upload_to_videos(instance, filename):
    if instance.created_by and instance.created_by.user_id:
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
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="accepted_cases", null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    case_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    accepted_date = models.DateTimeField(null=True, blank=True)
    document = models.FileField(upload_to=upload_to_documents, null=True, blank=True)
    image = models.ImageField(upload_to=upload_to_images, null=True, blank=True)
    video = models.FileField(upload_to=upload_to_videos, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        old_image = self.image.name if self.image else None
        old_document = self.document.name if self.document else None
        old_video = self.video.name if self.video else None

        super().save(*args, **kwargs)

        if is_new:
            for field_name, old_name in [('image', old_image),
                                        ('document', old_document),
                                        ('video', old_video)]:
                if old_name and 'temp' in old_name:
                    field = getattr(self, field_name)
                    new_name = old_name.replace('case_temp', f'case_{self.id}')
                    
                    new_path = os.path.join(settings.MEDIA_ROOT, new_name)
                    os.makedirs(os.path.dirname(new_path), exist_ok=True)
                    
                    old_path = os.path.join(settings.MEDIA_ROOT, old_name)
                    if os.path.exists(old_path):
                        os.rename(old_path, new_path)
                        field.name = new_name
                        self.save(update_fields=[field_name])

class CaseAttachment(models.Model):
    case = models.ForeignKey(Case, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='case_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Attachment for Case {self.case.id} - {self.file.name}"