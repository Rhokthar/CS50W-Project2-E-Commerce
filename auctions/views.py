from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm

from .models import Listing, User
from .forms import *


# CREATE LISTING FUNCTION STARTS
def CreateListing(request):
    # POST METHOD
    if request.method == "POST":
        listingForm = ListingForm(request.POST)
        # Check if Data is Valid
        if listingForm.is_valid():
            # Try creating listing
            try:
                listing = Listing()
                listing.title = listingForm.cleaned_data["title"]
                listing.description = listingForm.cleaned_data["description"]
                listing.price = listingForm.cleaned_data["price"]
                listing.user = request.user
                listing.imageURL = listingForm.cleaned_data["imageURL"]
                listing.category = listingForm.cleaned_data["category"]
                
                # Save Record in DB
                listing.save()
            # Error
            except:
                return render(request, "auctions/new-listing.html", {
                    "error": "Something went wrong."
                })
            
            return render(request, "auctions/index.html", {
                "successMessage": "Listing created successfully!"
            })
    
    # GET METHOD
    # User Not Authenticated
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    return render(request, "auctions/new-listing.html", {
        "form": ListingForm()
    })
# CREATE LISTING FUNCTION ENDS


# INDEX FUNCTION STARTS
def index(request):
    # Creare una lista con tutti i listing
    # In ogni listing mandato, devo far vedere il titolo, una breve descrizione, prezzo e foto
    return render(request, "auctions/index.html")
# INDEX FUNCTION ENDS


# LOGIN VIEW FUNCTION STARTS
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")
# LOGIN VIEW FUNCTION ENDS


# LOGOUT VIEW FUNCTION STARTS
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
# LOGOUT VIEW FUNCTION ENDS


# REGISTER FUNCTION STARTS
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
# REGISTER FUNCTION ENDS
