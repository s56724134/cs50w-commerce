from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    pass

#Category model
class Category(models.Model):
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return self.name

class Bid(models.Model):
    amount = models.FloatField(default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now())
    
    def __str__(self):
        return str(self.amount)
        
#AuctionList model
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='', related_name='auctions')
    starting_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, null=True, blank=True)
    image = models.CharField(max_length=1000, default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')
    date_created = models.DateTimeField(default=datetime.datetime.now())
    is_closed = models.BooleanField(default=False)
    watchlist = models.ManyToManyField(User, null=True, related_name="listingWatchlist")
    
    def __str__(self):
        return self.title
        
    
        
class Review(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    value = models.CharField(max_length=200)
    
    def __str__(self):
        return self.value
    