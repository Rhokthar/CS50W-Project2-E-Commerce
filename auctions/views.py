from unicodedata import category
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required 

from .models import Listing, User
from .forms import *


# CLOSE LISTING FUNCTION STARTS
@login_required
def CloseListing(request):
    # Utente che ha creato il listing può chiuderla
    closeListingID = Listing.objects.get(id=request.POST["close-listing"])
    
    # Listing disabilitata
    closeListingID.openListing = False
    closeListingID.save()

    messages.success(request, "Listing closed successfully!")
    return HttpResponseRedirect(reverse('listing-page', args=[closeListingID.id]))
# CLOSE LISTING FUNCTION ENDS


# COMMENT FUNCTION STARTS
@login_required
def CommentHandler(request):
    # Deve prendere l'utente che ha fatto il commento
    commentUser = User.objects.get(id=request.POST["comment-user"])
    print(commentUser.username)
    # Deve prendere l'oggetto su cui è stato fatto il commento
    commentListing = Listing.objects.get(id=request.POST["comment-listing"])
    print(commentListing.id)
    # Deve prendere il commento effettivo
    commentContent = request.POST["comment-content"]
    print(commentContent)

    # Deve aggiungere tutto ciò alla table dei commenti
    Comment.objects.create(user=commentUser, listing=commentListing, comment=commentContent)
    
    return HttpResponseRedirect(reverse('listing-page', args=[request.POST["comment-listing"]]))
    # BUGGIA QUESTO VA FATTO SULLA INDEX
    # Se get, deve displayare tutti i commenti su quell'oggetto
        # Dovrà passare chi ha fatto il commento
        # Dovrà passare l'effettivo commento
# COMMENT FUNCTION ENDS


# CREATE LISTING FUNCTION STARTS
@login_required
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
                    "error": "Something went wrong.",
                    "form": listingForm
                })
            
            return HttpResponseRedirect(reverse("index"))
    
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
    listingList = Listing.objects.all().order_by("-id")
    return render(request, "auctions/index.html", {
        "listingList": listingList
    })
# INDEX FUNCTION ENDS


# LISTING PAGE FUNCTION STARTS
def ListingsPage(request, id):
    # Vars
    listing = Listing.objects.get(id=id)
    winner = None

    # Listing Closed -> Search Winner
    if listing.openListing == False:
        # At Least One Bid
        try:
            winner = Bid.objects.filter(listing=listing).latest("offer")
        # Not a Single Bid
        except:
            winner = None

    return render(request, "auctions/listing-page.html", {
        "listing": listing,
        "winner": winner,
        "comments": Comment.objects.filter(listing=listing).all() 
    })
# LISTING PAGE FUNCTION ENDS


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


# NEW BID FUNCTION STARTS
@login_required
def NewBid(request):
    # Vars
    bidAmount = request.POST["bid-value"]
    bidUser = User.objects.get(id=request.POST["user-id"])
    bidListing = Listing.objects.get(id=request.POST["bid-item"])
    
    # Handling Errors
    # Non Numeric Value
    try:
        bidAmount = float(bidAmount)
    except:
        messages.error(request, "You can't insert a non-numeric value in the 'Bid' field.")
        return HttpResponseRedirect(reverse('listing-page', args=[request.POST["bid-item"]]))
    # Value 0 or Negative
    if bidAmount <= 0:
        messages.error(request, "You can't insert a null or negative value for the bid.")
        return HttpResponseRedirect(reverse('listing-page', args=[request.POST["bid-item"]]))
    # Value Less then Actual Bid
    if bidAmount <= bidListing.price:
        messages.error(request, "Your new bid must be higher then the actual price.")
        return HttpResponseRedirect(reverse('listing-page', args=[request.POST["bid-item"]]))

    # Inserting Bid into DB
    Bid.objects.create(user=bidUser, listing=bidListing, offer=bidAmount)
    # Updating Listing Price
    bidListing.price = bidAmount
    bidListing.save()  
    
    # Redirect
    messages.success(request, "Your bid has been saved. The price of the listing has been updated")
    return HttpResponseRedirect(reverse('listing-page', args=[request.POST["bid-item"]]))
# NEW BID FUNCTION ENDS


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


# WATCHLIST HANDLING FUNCTION STARTS
@login_required
def WatchlistHandler(request):
    # POST Method
    if request.method == "POST":
        listingItem = Listing.objects.get(id=request.POST["watchlist-item"])
        watchlistUser = User.objects.get(id=request.POST["user-id"])

        # Add to Watchlist
        if request.POST["handling-type"] == "add":            
            watchlistUser.watchlist.add(listingItem)
            watchlistUser.save()

            return HttpResponseRedirect(reverse("watchlist"))
        # Remove from Watchlist
        else:
            watchlistUser.watchlist.remove(listingItem)
    
    # GET Method
    return render(request, "auctions/watchlist.html")
# WATCHLIST HANDLING FUNCTION ENDS
