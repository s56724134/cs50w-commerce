from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Bid, Review



def listing(request,pk):
    listingData = Listing.objects.get(id=pk)
    isListingWatchlist = request.user in listingData.watchlist.all()
    allReview = Review.objects.filter(auction=listingData)
    isOwner = request.user.username == listingData.owner.username
    context = {
        "listing":listingData, 
        "isListingWatchlist":isListingWatchlist,
        "allReview":allReview,
        "isOwner":isOwner,
        }
    return render(request, "auctions/listing.html", context)

def closeAuction(request, pk):
    listingData = Listing.objects.get(id=pk)
    listingData.is_closed = True
    listingData.save()
    isOwner = request.user.username == listingData.owner.username
    isListingWatchlist = request.user in listingData.watchlist.all()
    allReview = Review.objects.filter(auction=listingData)
    context = {
        "listing":listingData, 
        "isListingWatchlist":isListingWatchlist,
        "allReview":allReview,
        "isOwner":isOwner,
        "update":True,
        "message":"Congreatulation! Your auction is closed."
        }
    return render(request, "auctions/listing.html", context)
    
def addBid(request, pk):
    newBid = request.POST["addBid"]
    listingData = Listing.objects.get(id=pk)
    isOwner = request.user.username == listingData.owner.username
   
    if int(newBid) > listingData.starting_bid.amount:
        updatedBid = Bid(bidder=request.user, amount=int(newBid))
        updatedBid.save()
        listingData.starting_bid = updatedBid
        listingData.save()
        return render(request, "auctions/listing.html",{
            "listing":listingData,
            "message": "Bid was updated successfully",
            "updated":True,
            "isOwner":isOwner
        })
    else:
        return render(request, "auctions/listing.html",{
            "listing":listingData,
            "message": "Bid was updated failed",
            "updated":False,
            "isOwner":isOwner
        })
        

def addReview(request, pk):
    currentUser = request.user
    listingData = Listing.objects.get(id=pk)
    message = request.POST["addReview"]
    
    newReview = Review(
        owner = currentUser,
        auction = listingData,
        value = message,
    )
    newReview.save()
    return HttpResponseRedirect(reverse("listing",args=(pk, )) )  
    
def displayWatchlist(request):
    listingData = Listing.objects.filter(watchlist=request.user)
    context = {"Listing":listingData}
    return render(request, "auctions/watchlist.html", context)

def removeWatchlist(request, pk):
    if request.method == "POST":
        listingData = Listing.objects.get(id=pk)
        currentUser = request.user
        listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(pk, )) )  
   
def addWatchlist(request, pk):
    if request.method == "POST":
        listingData = Listing.objects.get(id=pk)
        currentUser = request.user
        listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(pk, )) )  
    

def index(request):
    activeListing = Listing.objects.filter(is_closed=False) 
    allcategories = Category.objects.all()
    
    context = {"Listing": activeListing, "categories":allcategories}
    return render(request, "auctions/index.html", context)
    
def display_category(request):
    if request.method == "POST":
        categoryFromForm = request.POST["category"]
        category = Category.objects.get(name=categoryFromForm)
        activeListing = Listing.objects.filter(is_closed=False, category=category) 
        allcategories = Category.objects.all()
        context = {"Listing": activeListing, "categories":allcategories}
        return render(request, "auctions/index.html", context)
    

def create_listing(request):
    allcategories = Category.objects.all()
    # get the data from the form
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["price"]
        category = request.POST["category"]
        # who is user?
        currentUser = request.user
        #Get all content about the paticular Category
        categoryData = Category.objects.get(name=category)
        # Create a bid object
        bid = Bid(amount=(float(price)), bidder=currentUser)
        bid.save()
        # Create a new Listing object
        newListing = Listing(
            title=title,
            image=image,
            description=description,
            starting_bid=bid,
            category=categoryData,
            owner=currentUser)
        newListing.save()
        #Redirect to index page
        return HttpResponseRedirect(reverse("index"))
    
    context = {"categories":allcategories}
    return render(request, "auctions/create-listing.html", context)

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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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


    