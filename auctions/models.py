from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    

class Auction(models.Model): 
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=80)
    bid = models.IntegerField()
    image = models.URLField(blank=True, max_length=200)
    category = models.CharField(blank=True, max_length=15)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="person")
    is_active = models.BooleanField(default=True)

class Bids(models.Model): 
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bid = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='total_bids')

class Watchlist(models.Model): 
    user_list = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userlist")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auctionlist")

    def __str__(self): 
        return str(self.auction)


class Comments(models.Model): 
    comment_list = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=250, blank=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mr_comment")
