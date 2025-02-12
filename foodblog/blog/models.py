from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
import math

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Foodblog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)  # Auto-generated slug for URLs
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    description = models.TextField()  # Can store Markdown/HTML
    meta_description = models.CharField(max_length=160, blank=True, null=True)  # SEO meta description
    ingredients = models.JSONField()  # Stores structured ingredients
    instructions = models.JSONField()  # Stores structured steps
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="foodblogs")
    tags = ArrayField(models.CharField(max_length=30), blank=True, null=True)  # For filtering & search
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Auto-generate slug from title before saving."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def estimated_read_time(self):
        """Estimate read time based on word count."""
        word_count = len(self.description.split()) + len(str(self.ingredients).split()) + len(str(self.instructions).split())
        return math.ceil(word_count / 200)  # Assuming 200 words per minute reading speed

    def __str__(self):
        return self.title
