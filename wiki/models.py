from django.db import models

class Law(models.Model):
    TYPE_CHOICES = [
        ('family', 'Family Law'),
        ('criminal', 'Criminal Law'),
        ('civil', 'Civil Law'),
        ('labor', 'Labor Law'),
        ('commercial', 'Commercial and Business Law'),
        ('other', 'Others'),
    ]

    title = models.CharField(max_length=255)
    code = models.CharField(max_length=100)
    full_law = models.TextField()
    tags = models.TextField()  
    case_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.title


class Summary(models.Model):
    law = models.OneToOneField(Law, on_delete=models.CASCADE, related_name='summary')
    summary = models.TextField()

    def __str__(self):
        return f"Summary of {self.law.title}"


class Translation(models.Model):
    law = models.OneToOneField(Law, on_delete=models.CASCADE, related_name='translation')
    language_tagalog = models.TextField(blank=True, null=True)
    language_bisaya = models.TextField(blank=True, null=True)
    language_waray = models.TextField(blank=True, null=True)
    language_chavacano = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Translations of {self.law.title}"


class OFWSupportDetail(models.Model):
    country = models.CharField(max_length=100)
    support_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField()
    contact_number = models.TextField()
    email_address = models.TextField()
    website = models.TextField(blank=True, null=True)
    available_services = models.TextField()
    working_hours = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.support_name} - {self.country}"
