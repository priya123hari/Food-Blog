from django.db import models
from django.utils.text import slugify
import math

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Foodblog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    description = models.TextField()
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    ingredients = models.JSONField(default=dict, blank=True, null=True)
    instructions = models.JSONField(default=dict, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="foodblogs")
    tags = models.JSONField(default=list, blank=True, null=True)  # Changed from ArrayField
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def estimated_read_time(self):
        word_count = len(self.description.split()) + len(str(self.ingredients).split()) + len(str(self.instructions).split())
        return math.ceil(word_count / 200)  # Assuming 200 words per minute

    def __str__(self):
        return self.title
