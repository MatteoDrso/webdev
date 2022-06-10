from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth import settings

class Comment(models.Model):
	#parent = models.ForeignKey(Comment) #does that make sense?
	publisher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null = True,
    ) #not sure if this works properly. source: https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#referencing-the-user-model
	title = models.CharField(max_length=200)
	message = models.TextField()
	publication_date = models.DateTimeField()

	def __str__(self):
		return self.title, self.message()