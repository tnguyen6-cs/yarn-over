from django.db import models

# Create your models here.
class Category(models.Model):
    'id'
    cate = models.CharField(max_length=255)
    def __str__(self):
        return f"{{self.cate}}"
        
class PatternTable(models.Model):
    'id'
    name = models.CharField(max_length=255, unique=True)
    link = models.TextField()
    description = models.TextField()
    #category = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="patterns_incategory")
    

    def __str__(self):
        return f"{self.name}"

