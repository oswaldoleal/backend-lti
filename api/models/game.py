from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField()
    svg_route = models.CharField(max_length=200)
