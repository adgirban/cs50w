from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
    
class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True, related_name="userBid")

    

class Listings(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    availability = models.BooleanField(default = True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank = True, null = True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="userWatchlist")

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True, related_name="userComment")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, blank = True, null = True, related_name="listingComment")
    message = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.author} : {self.listing}"
    

