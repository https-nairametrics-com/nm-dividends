from django.db import models
from authentication.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.postgres.fields.jsonb import JSONField
from django.utils.translation import gettext_lazy as _
# Create your models here.


class NMData(models.Model):
    STATUS_OPTIONS = [
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('disapproved', 'disapproved'),
    ]
    name = models.CharField(max_length=255)  # CSV name
    data_type = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # Additional field
    upload_date = models.DateField(auto_now_add=True)  # Auto-populated date
    csv_file = models.FileField(upload_to='uploads/')  # Uploaded file
    project_status = models.CharField(
        choices=STATUS_OPTIONS, max_length=255, default="not started")
    json_data = models.JSONField(blank=True, null=True)  # Parsed JSON data from the CSV

    def __str__(self):
        return self.name