from django.db import models

# Create your models here.
class PatternTable(models.Model):
    pid = models.Field(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    link = models.TextField()
    description = models.TextField()
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
