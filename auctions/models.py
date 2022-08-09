from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Id
    # Username
    # Password
    # E-mail
    pass

class Listing(models.Model):
    # Id - Automatic
    # Choices Vars
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
    # Titolo
    title = models.CharField("Title", max_length=128, default=None)
    # Descrizione
    description = models.TextField("Description", max_length=1024, default=None)
    # Prezzo
    price = models.FloatField("Price")
    # Venditore
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Immagine
    imageURL = models.URLField(default="https://www.svaghiamo.it/noleggio-calcio-balilla-4-contro-4/image-not-found-4a963b95bf081c3ea02923dceaeb3f8085e1a654fc54840aac61a57a60903fef/#iLightbox[postimages]/0")
    # Categoria
    category = models.CharField(max_length=64, choices=CATEGORIES_CHOICES, default=HOM)

class Bid(models.Model):
    # ID - Automatic
    # Who does the Bid
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # On Which Bid
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    # How Much
    offer = models.FloatField("Offer")
    pass
class Comment(models.Model):
    pass
