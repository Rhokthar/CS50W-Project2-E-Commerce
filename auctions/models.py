from django.contrib.auth.models import AbstractUser
from django.db import models

# USER MODEL STARTS
class User(AbstractUser):
    # Id
    # Username
    # Password
    # E-mail
    def __str__(self):
        return f"{id}"
# USER MODEL ENDS


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # IMG
    imageURL = models.URLField("Image URL", default="https://www.svaghiamo.it/noleggio-calcio-balilla-4-contro-4/image-not-found-4a963b95bf081c3ea02923dceaeb3f8085e1a654fc54840aac61a57a60903fef/#iLightbox[postimages]/0")
    # Category
    category = models.CharField(max_length=64, choices=CATEGORIES_CHOICES, default=HOM)
# LISTING CLASS ENDS


# BID MODEL STARTS
class Bid(models.Model):
    # ID - Automatic
    # Who does the Bid
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # On Which Bid
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    # How Much
    offer = models.FloatField()
# BID MODEL ENDS


# COMMENTS MODEL STARTS
class Comment(models.Model):
    pass
# COMMENTS MODEL ENDS

