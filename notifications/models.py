from django.db import models
from django.conf import settings

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('case_assigned', 'Case Assigned'),
        ('case_status', 'Case Status Update'),
        ('message', 'New Message'),
        ('system', 'System Notification'),
        ('other', 'Other'),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_object_id = models.CharField(max_length=255, null=True, blank=True)
    related_object_type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} - {self.recipient.email}"

    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])
