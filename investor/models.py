from unittest.util import _MAX_LENGTH
from django.db import models
from authentication.models import User

# Create your models here.


class Interest(models.Model):
    interest = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='created_by_investor_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.amount


class Risk(models.Model):
    risk = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='created_by_investor_risk')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.risk


class InvestmentSize(models.Model):
    investment_size = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='created_by_investor_size')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.investment_size


class Period(models.Model):
    period = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='created_by_investor_period')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.period


class Expectations(models.Model):
    expectation = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='created_by_investor_expectation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.expectation


class Investor(models.Model):
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='owner_investor_set')
    expectation = models.ForeignKey(to=Expectations, on_delete=models.CASCADE)
    period = models.ForeignKey(to=Period, on_delete=models.CASCADE)
    investment_size = models.ForeignKey(
        to=InvestmentSize, on_delete=models.CASCADE)
    serialkey = models.CharField(max_length=255, null=True)
    risk = models.ForeignKey(to=Risk, on_delete=models.CASCADE)
    interest = models.ForeignKey(to=Interest, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='approved_by_investor_set')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.created_at
