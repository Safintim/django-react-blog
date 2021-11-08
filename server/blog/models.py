from django.db import models

POST_TITLE_MAX_LENGTH = 150


class Post(models.Model):
    title = models.CharField(max_length=POST_TITLE_MAX_LENGTH)
    text = models.TextField()

    def __str__(self) -> str:
        return self.title
