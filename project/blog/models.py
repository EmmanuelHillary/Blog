from django.db import models
import math
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from .validators import validate_file_extension, validate_file_type


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='profile photos/')

    def __str__(self):
        return f'Profile of {self.user.username}'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    objects = models.Manager()
    published = PublishedManager()
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Draft')
    restrict_comments = models.BooleanField(default=False)
    favourite = models.ManyToManyField(User, related_name='favourites', blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_edit_url(self):
        return reverse('post:edit', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def time(self):
        now = timezone.now()

        diff = now - self.updated

        if diff.days == 0 and 0 <= diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and 60 <= diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and 3600 <= diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if 1 <= diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if 30 <= diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


class PostImage(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image = models.FileField(upload_to='post images/', blank=True, null=True, validators=[validate_file_type])

    def __str__(self):
        return self.post.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField(max_length=180)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post.title} - {self.user.username}'

    def time(self):
        now = timezone.now()

        diff = now - self.timestamp

        if diff.days == 0 and 0 <= diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and 60 <= diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and 3600 <= diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if 1 <= diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if 30 <= diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


@receiver(pre_save, sender=Post)
def slug_title(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug


@receiver(post_save, sender=User)
def profile_create(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])