from django.contrib.auth.models import AbstractUser
from django.db import models


# BID MODEL STARTS
class Bid(models.Model):
    # ID - Automatic
    # Who does the Bid
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    # On Which Bid
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)
    # How Much
    offer = models.FloatField()
# BID MODEL ENDS


# COMMENTS MODEL STARTS
class Comment(models.Model):
    # ID
    # User che ha fatto il commento
    user = models.ForeignKey("User", on_delete=models.CASCADE, default=None)
    # Su che oggetto ha fatto il commento
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, default=None)
    # Contenuto del commento
    comment = models.TextField("Comment", max_length=1024, default=None, null=False, blank=False)
# COMMENTS MODEL ENDS


# Choices Vars for Listing
FSH = "Fashion"
TOY = "Toys"
HOM = "Home"
ELE = "Electronics"
CATEGORIES_CHOICES = (
    (FSH, "Fashion"),
    (TOY, "Toys"),
    (HOM, "Home"),
    (ELE, "Electronics"),
)
# LISTING CLASS STARTS
class Listing(models.Model):
    # Id - Automatic
    # Title
    title = models.CharField("Title", max_length=128, default=None)
    # Description
    description = models.TextField("Description", max_length=1024, default=None)
    # Price
    price = models.FloatField("Price")
    # Seller
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    # IMG
    imageURL = models.URLField("Image URL", default=None, blank=True, null=True)
    # Category
    category = models.CharField(max_length=64, choices=CATEGORIES_CHOICES, default=HOM)
    # Open/Closed
    openListing = models.BooleanField(default=True)
# LISTING CLASS ENDS


# USER MODEL STARTS
class User(AbstractUser):
    # Id
    # Username
    # Password
    # E-mail
    # Watchlist
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="watchlist")
    def __str__(self):
        return f"{id}"
# USER MODEL ENDS