# models.py
from django.db import models

class Law(models.Model):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=100)
    full_law = models.TextField()

class Summary(models.Model):
    law = models.OneToOneField(Law, on_delete=models.CASCADE, related_name='summary')
    summary = models.TextField()

class Translation(models.Model):
    law = models.OneToOneField(Law, on_delete=models.CASCADE, related_name='translation')
    language_tagalog = models.TextField(blank=True, null=True)
    language_bisaya = models.TextField(blank=True, null=True)
    language_waray = models.TextField(blank=True, null=True)
