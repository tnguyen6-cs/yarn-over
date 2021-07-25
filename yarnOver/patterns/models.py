from django.db import models

# Create your models here.
class PatternTable(models.Model):
    name = models.CharField(max_length=255)
    link = models.TextField()
    description = models.TextField()
    category = models.CharField(max_length=255)
