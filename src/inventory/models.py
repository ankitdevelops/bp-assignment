from django.db import models
from django.utils.text import slugify


class Item(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Item, self).save(*args, **kwargs)
