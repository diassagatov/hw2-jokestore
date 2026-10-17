from django.db import models


class JokeStore(models.Model):
    text = models.TextField(verbose_name="joke")
    likes = models.PositiveIntegerField(default=0, verbose_name="likes")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created at")

    def __str__(self):
        return f'self.text[:50], self.likes'
