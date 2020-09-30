from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Model for Auction Listings
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    category = models.CharField(max_length=64)
    image = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f"{self.id}: {self.title} is an Auction in the {self.category} category, created by {self.user}."

# Model for Bids
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.IntegerField()

    def __str__(self):
        return f"Auction #{self.listing.id} Has a bid of {self.bid}, made by {self.user}."

# Model for Comments on Auctions
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    text = models.CharField(max_length=256)
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user} made a comment on Auction #{self.listings.id}."
