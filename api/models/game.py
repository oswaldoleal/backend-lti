from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField()
    image_url = models.CharField(max_length=300)
