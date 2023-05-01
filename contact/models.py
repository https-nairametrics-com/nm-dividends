from django.db import models
from authentication.models import User

# Create your models here.


class Contact(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='contact_authentication_set')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.subject)
