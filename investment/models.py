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


def identity_to(instance, filename):
    return 'identity/{filename}'.format(filename=filename)


class Currency(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DealType(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MainRoom(models.Model):
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


class InvestmentRoom(models.Model):
    name = models.CharField(max_length=255)
    main_room = models.ForeignKey(
        to=MainRoom, null=True, on_delete=models.CASCADE, related_name='main_room')
    slug = models.SlugField(max_length=255, null=True, unique=True)
    description = models.TextField(null=True)
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='main_created_by')
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
    TYPE_OPTIONS = [
        ('not started', 'not started'),
        ('started', 'started'),
        ('pending', 'pending'),
        ('in progress', 'in progress'),
        ('approved', 'approved'),
        ('completed', 'completed'),
    ]
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=255)
    amount = models.IntegerField(null=True)
    project_cost = models.IntegerField(null=True)
    project_raise = models.IntegerField(null=True)
    milestone = models.IntegerField(null=True)
    minimum_allotment = models.IntegerField(null=True)
    maximum_allotment = models.IntegerField(null=True)
    slug = models.SlugField(max_length=255, null=True, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=255, null=True)
    video = models.CharField(max_length=255, null=True)
    room = models.ForeignKey(to=InvestmentRoom, on_delete=models.CASCADE)
    offer_period = models.DateField(null=True)
    period = models.ForeignKey(
        to=Period, on_delete=models.CASCADE, related_name='investment_period')
    periodic_payment = models.DecimalField(
        max_digits=6, default=1, decimal_places=2)
    currency = models.ForeignKey(
        to=Currency, null=True, on_delete=models.CASCADE, related_name='investment_currency')
    dealtype = models.ForeignKey(
        to=DealType, null=True, on_delete=models.CASCADE, related_name='investment_dealtype')
    volume = models.IntegerField(null=True)
    only_returns = models.BooleanField(default=True)
    off_plan = models.BooleanField(default=False)
    outright_purchase = models.BooleanField(default=True)
    outright_purchase_amount = models.IntegerField(null=True)
    offer_price = models.IntegerField(null=True)
    spot_price = models.IntegerField(null=True)
    unit_price = models.IntegerField(null=True)
    roi = models.DecimalField(max_digits=6, decimal_places=2)
    annualized = models.DecimalField(max_digits=6, decimal_places=2)
    risk = models.ForeignKey(to=Risk, on_delete=models.CASCADE)
    features = models.TextField(null=True)
    is_verified = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    title_status = models.CharField(
        choices=TYPE_OPTIONS, max_length=255, default="pending")
    construction_status = models.CharField(
        choices=TYPE_OPTIONS, max_length=255, default="pending")
    project_status = models.CharField(
        choices=TYPE_OPTIONS, max_length=255, default="not started")
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
    TYPE_OPTIONS = [
        ('only returns', 'only returns'),
        ('off plan', 'off plan'),
        ('outright purchase', 'outright purchase')
    ]
    investment = models.ForeignKey(
        to=Investment, related_name='investment', on_delete=models.CASCADE)
    investor = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='investor')
    amount = models.IntegerField(null=True)
    bid_price = models.IntegerField(null=True)
    slug = models.CharField(max_length=255, null=True)
    investment_type = models.CharField(
        choices=TYPE_OPTIONS, max_length=255, default="only returns")
    volume = models.IntegerField(default=1)
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
        return str(self.amount)


class Installment(models.Model):
    investor = models.ForeignKey(
        to=Investors, on_delete=models.CASCADE, related_name='investor_instalmment')
    amount = models.IntegerField(null=True)
    serialkey = models.CharField(max_length=255, null=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=True, related_name='approved_by_installment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.amount)


class Mfa(models.Model):
    user = models.ForeignKey(
        to=User, related_name='mfa_key', on_delete=models.CASCADE)
    mfa = models.CharField(max_length=255)
    is_open = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mfa


class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    nin = models.CharField(max_length=255, unique=True, db_index=True)
    phone = models.CharField(max_length=255, null=True)
    dob = models.DateField(null=True)
    address = models.TextField(null=True)
    is_verified = models.BooleanField(default=False)
    identity = models.ImageField(
        _("Identity"), upload_to=identity_to, default='identity/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SponsorInvestment(models.Model):
    investment = models.ForeignKey(
        to=Investment, related_name='investment_sponsorinvestment', on_delete=models.CASCADE)
    sponsor = models.ForeignKey(
        to=Sponsor, related_name='sponsor_sponsorinvestment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)
