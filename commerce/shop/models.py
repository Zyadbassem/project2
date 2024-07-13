from django.db import models

# Create your models here.
class user(models.Model):
    username = models.CharField(max_length=32)
    hashPassword = models.CharField(max_length=64)
    def __str__(self):
        return self.username