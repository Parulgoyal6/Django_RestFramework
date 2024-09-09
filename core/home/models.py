from django.db import models

# Create your models here.

class Color(models.Model):
    Color_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.Color_name
class Person(models.Model):
    color = models.ForeignKey(Color, on_delete=models.CASCADE , related_name="color")
    name = models.CharField(max_length=100)
    age = models.IntegerField()
