from django.db import models
from authentication.models import User
from django.utils.text import slugify

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)  # Slug field
    content = models.TextField()  # This will store the body content (including HTML)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(upload_to='featured_images/', null=True, blank=True)  # Optional featured image

    def save(self, *args, **kwargs):
        if not self.slug:  # Automatically generate a slug if it isn't provided
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
