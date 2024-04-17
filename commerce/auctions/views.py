from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listings, Comment, Bid


def index(request):
    active = Listings.objects.filter(availability = True)
    return render(request, "auctions/index.html", {
        "listings": active
    })


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
    

def create(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })
    else:
        name = request.POST["name"]
        description = request.POST["description"]
        url = request.POST["imageURL"]
        price = request.POST["price"]
        category = request.POST["category"]

        user = request.user

        categoryX = Category.objects.get(name=category)

        bid = Bid(bid=float(price), user=user)
        bid.save()

        newListing = Listings(name=name, description=description, image=url, price=bid, category=categoryX, owner=user)

        newListing.save()
        return HttpResponseRedirect(reverse("index"))
    

def category(request):
    if request.method == "POST":
        categoryForm = request.POST["category"]
        categoryData = Category.objects.get(name = categoryForm)
        active = Listings.objects.filter(availability = True, category = categoryData)
        categories = Category.objects.all()
        return render(request, "auctions/category.html", {
            "listings": active,
            "categories": categories
        })
    else:
        active = Listings.objects.filter(availability = True)
        categories = Category.objects.all()
        return render(request, "auctions/category.html", {
            "listings": active,
            "categories": categories
        })
    
def listing(request, id):
    listing = Listings.objects.get(pk=id)
    inWatchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing = listing)
    isOwner = request.user.username == listing.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "inWatchlist": inWatchlist,
        "comments": comments,
        "isOwner": isOwner
    })

def remove(request, id):
    listing = Listings.objects.get(pk=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def add(request, id):
    listing = Listings.objects.get(pk=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def display(request):
    user = request.user
    listings = user.userWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def addComment(request, id):
    user = request.user
    listing = Listings.objects.get(pk=id)
    message = request.POST["comment"]

    newComment = Comment(author=user, listing=listing, message=message)
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def addBid(request,id):
    listing = Listings.objects.get(pk=id)
    bid = request.POST["bid"]
    inWatchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing = listing)

    if float(bid) > listing.price.bid:
        updateBid = Bid(user = request.user, bid = float(bid))
        updateBid.save()
        listing.price = updateBid
        listing.save()
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Bid Successful",
            "update": True,
            "inWatchlist": inWatchlist,
            "comments": comments
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Bid Failed",
            "update": False,
            "inWatchlist": inWatchlist,
            "comments": comments
        })
    
def closeBid(request, id):
    listing = Listings.objects.get(pk=id)
    listing.availability = False
    listing.save()
    inWatchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing = listing)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "message": "The bid was successfully closed.",
        "update": True,
        "inWatchlist": inWatchlist,
        "comments": comments
    })

