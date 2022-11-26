from email.policy import default
from django.db import models
from authentication.models import User
from investor.models import Period, Risk
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields.jsonb import JSONField
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.


def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)


class InvestmentRoom(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, unique=True)
    description = models.TextField(null=True)
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('room_detail', kwargs={'slug': self.slug})


class Investment(models.Model):
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=255, null=True)
    room = models.ForeignKey(to=InvestmentRoom, on_delete=models.CASCADE)
    period = models.ForeignKey(
        to=Period, on_delete=models.CASCADE, related_name='investment_period')
    amount = models.IntegerField(null=True)
    roi = models.CharField(max_length=255)
    annualized = models.CharField(max_length=255)
    risk = models.ForeignKey(to=Risk, on_delete=models.CASCADE)
    features = models.TextField(null=True)
    is_verified = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('investment_detail', kwargs={'slug': self.slug})


class Gallery(models.Model):
    investment = models.ForeignKey(
        to=Investment, on_delete=models.CASCADE, related_name='gallery_set')
    gallery = models.ImageField(
        _("Gallery"), upload_to=upload_to, default='post/default.jpg')
    #gallery = models.CharField(max_length=255)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.gallery)


class Investors(models.Model):
    investment = models.ForeignKey(
        to=Investment, related_name='investment', on_delete=models.CASCADE)
    investor = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='investor')
    amount = models.IntegerField(null=True)
    slug = models.CharField(max_length=255, null=True)
    serialkey = models.CharField(max_length=255, null=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=True, related_name='approved_by')
    is_closed = models.BooleanField(default=False)
    closed_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=True, related_name='closed_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.amount


class Mfa(models.Model):
    user = models.ForeignKey(
        to=User, related_name='mfa_key', on_delete=models.CASCADE)
    mfa = models.CharField(max_length=255)
    is_open = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mfa
