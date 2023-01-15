from django.db import models
from investment.models import Investors, Investment
from django.utils.text import slugify
from django.urls import reverse
from authentication.models import User

# Create your models here.


class Comment(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    comment = models.TextField(null=True)
    investment = models.ForeignKey(
        to=Investment, null=True, on_delete=models.CASCADE, related_name='investments_comment')
    investor = models.ForeignKey(
        to=Investors, null=True, on_delete=models.CASCADE, related_name='investment_comment')
    responded_by = models.ForeignKey(null=True,
                                     to=User, on_delete=models.CASCADE, related_name='user_comment')
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug
