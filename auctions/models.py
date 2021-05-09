from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=300)
    starting_bid = models.FloatField()
    listing_picture = models.URLField()
    category = models.CharField(max_length=64, default='uncatogarized')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="listing_winner")

    def __str__(self):
        return f"{self.id}: {self.title} - {self.starting_bid}"


class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    # user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='watcher', null=True)
    listing = models.ManyToManyField(Listing)

    def __str__(self):
        return f"{self.user}'s WatchList"


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.CharField(max_length=64)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} Comments"


class Bid(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bid_listing")
    user = models.CharField(max_length=64)
    bid = models.FloatField()

    def __str__(self):
        return f"{self.listing.title} bid amount {self.bid} by {self.user}"
