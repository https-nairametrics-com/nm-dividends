from email.policy import default
from django.db import models
from authentication.models import User
from investor.models import Period, Risk


# Create your models here.

class InvestmentRoom(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Investment(models.Model):
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=255)
    description = models.TextField()
    room = models.ForeignKey(to=InvestmentRoom, on_delete=models.CASCADE)
    period = models.ForeignKey(to=Period, on_delete=models.CASCADE)
    amount = models.CharField(max_length=255)
    roi = models.CharField(max_length=255)
    annualized = models.CharField(max_length=255)
    risk = models.ForeignKey(to=Risk, on_delete=models.CASCADE)
    features = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    investment = models.ForeignKey(
        to=Investment, on_delete=models.CASCADE, related_name='investment_investment_set')
    gallery = models.CharField(max_length=255)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.gallery


class Investors(models.Model):
    investment = models.ForeignKey(
        to=Investment, related_name='investment', on_delete=models.CASCADE)
    investor = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='investor')
    amount = models.CharField(max_length=255)
    serialkey = models.CharField(max_length=255, null=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='approved_by')
    is_closed = models.BooleanField(default=False)
    closed_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='closed_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.amount
