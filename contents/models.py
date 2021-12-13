from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.contrib.auth.models import User


def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + get_random_string(length=5)
    return unique_slug


class Community(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeginKey(User, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Rules(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    rule = models.CharField(max_length=250)


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeginKey(Community, on_delete=models.CASCADE)
    joined = models.DateTimeField(auto_now_add=True)


class Blocked(models.Model):
    user = models.ForeginKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    reason = models.TextField()


class Post(models.Model):
    title = models.CharField(max_length=250)
    community = models.ForeignKey(Community, on_delete=models.CASCADE,
                                  related_name='posts')
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')
    body = models.TextField()
    image = models.ImageField(upload_to='posts/%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
