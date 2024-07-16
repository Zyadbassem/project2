from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32)
    hashPassword = models.CharField(max_length=64)
    def __str__(self):
        return self.username
    
class Item(models.Model):
    itemName = models.CharField(max_length=64)
    itemImage = models.URLField()
    itemprice = models.CharField(max_length=10)
    def __str__(self):
        return self.itemName
    
class Bid(models.Model):
    buyerId = models.ForeignKey(User, on_delete=models.CASCADE)
    itemId = models.ForeignKey(Item, on_delete=models.CASCADE)
    bidAmount = models.DecimalField(max_digits=10, decimal_places=2)