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
    original_post = models.ForeignKey(
    	'self',
    	on_delete=models.CASCADE,
    	null=True,
    	related_name='replies',
    )
    publisher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="comments",
    )
    title = models.CharField(
        max_length=200,
        null=True,
    )
    message = models.TextField()
    upvoters = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="upvotes",
    )
    downvoters = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="downvotes",
    )
    publication_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
    	if self.title == None:
    		return "No title given"
    	else:
        	return self.title


    def get_vote_count(self):
        return self.upvoters.count() - self.downvoters.count()