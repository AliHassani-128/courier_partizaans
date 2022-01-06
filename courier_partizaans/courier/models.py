from django.db import models

# Create your models here.

class Courier(models.Model):
    name = models.CharField(unique=True,max_length=128)

    def __str__(self):
        return self.name

