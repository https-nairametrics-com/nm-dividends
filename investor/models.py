from unittest.util import _MAX_LENGTH
from django.db import models
from authentication.models import User

# Create your models here.


class Interest(models.Model):
    interest = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(null=True,
                                   to=User, on_delete=models.CASCADE, related_name='created_by_investor_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)


class Risk(models.Model):
    risk = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(null=True,
                                   to=User, on_delete=models.CASCADE, related_name='created_by_risk_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.risk


class InvestmentSize(models.Model):
    investment_size = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(null=True,
                                   to=User, on_delete=models.CASCADE, related_name='created_by_size_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.investment_size


class Period(models.Model):
    period = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(null=True,
                                   to=User, on_delete=models.CASCADE, related_name='created_by_period_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.period


class Expectations(models.Model):
    expectation = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(null=True,
                                   to=User, on_delete=models.CASCADE, related_name='created_by_expectations_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.expectation


class InitialInterests(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='interest_authentication_set')
    risk = models.ForeignKey(
        to=Risk, on_delete=models.CASCADE, related_name='risk_authentication_set')
    period = models.ForeignKey(
        to=Period, on_delete=models.CASCADE, related_name='interest_period_set')
    interest = models.ForeignKey(
        to=Interest, on_delete=models.CASCADE, related_name='interest_interest_set')
    investmentsize = models.ForeignKey(
        to=InvestmentSize, on_delete=models.CASCADE, related_name='interest_size_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)
