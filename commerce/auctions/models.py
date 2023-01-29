from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category_name}"

class Listing(models.Model):
    listing_title = models.CharField(max_length=64)
    listing_description = models.CharField(max_length=500)
    listing_image = models.ImageField(null=True, blank=True, upload_to="images/")
    listing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    listing_starting_bid = models.IntegerField()
    listing_current_bid = models.IntegerField()
    listing_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    listing_watchlist = models.ManyToManyField(User, blank=True, related_name="wachtlist_items")
    listing_open = models.BooleanField()
    listing_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.listing_title}"

class Comment(models.Model):
    comment_content = models.CharField(max_length=255)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments", null=True)
    comment_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments", null=True)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment_content} by {self.comment_user} on listing {self.comment_listing}"

class Bid(models.Model):
    bid_value = models.IntegerField()
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids", null=True)
    bid_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids", null=True)
    bid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bid_value} by {self.bid_user} on {self.bid_listing}"
