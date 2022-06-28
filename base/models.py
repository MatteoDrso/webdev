from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth import settings


class Comment(models.Model):
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        related_name='+',
    )
    original_comment = models.ForeignKey(
    	'self',
    	on_delete=models.CASCADE,
    	null=True,
    	related_name='+',
    )
    publisher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="comments",
     )
    title = models.CharField(max_length=200)
    message = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
