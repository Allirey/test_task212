from django.conf import settings
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Article(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = 'published', 'Published'
        DRAFT = 'draft', 'Draft'

    title = models.CharField(max_length=255)
    body = RichTextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        permissions = [
            ('publish_without_moderation', 'Can publish without moderation'),
        ]
        ordering = ['-created', ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author, self.article)

    def get_absolute_url(self):
        return reverse('article_list')
