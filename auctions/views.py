from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm

from .models import User, Category, Listing, Comments, Bid




def listing(request, id):
    listingData = get_object_or_404(Listing, pk=id)  # Retourne une 404 si le listing n'existe pas
    isListingWatchList = request.user in listingData.watchlist.all()
    allComments = Comments.objects.filter(listing=listingData)
    isOwner=request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingWatchList,
        "allComments": allComments,
        "isOwner":isOwner
    })

def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False 
    listingData.save()
    isListingWatchList = request.user in listingData.watchlist.all()
    allComments = Comments.objects.filter(listing=listingData)
    isOwner=request.user.username == listingData.owner.username

    return render(request, "auctions/listing.html", {
    "listing": listingData,
    "isListingInWatchlist": isListingWatchList,
    "allComments": allComments,
    "isOwner":isOwner,
    "update":True,
    "message": "Congratulations! Your auction is closed."
    })



def addBid(request, id):
    newBid = request.POST["newBid"]
    listingData = Listing.objects.get(pk=id)
    isListingWatchList = request.user in listingData.watchlist.all()
    allComments = Comments.objects.filter(listing=listingData)
    isOwner=request.user.username == listingData.owner.username
    if int(newBid) > listingData.price.bid:
        updateBid = Bid(user=request.user, bid=int(newBid))
        updateBid.save()
        listingData.price = updateBid 
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid  updated successfully",
            "update": True,
            "isListingInWatchlist": isListingWatchList,
            "allComments": allComments,
            "isOwner":isOwner,

        })
    else:
            return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid updated failed",
            "update": False,
            "isListingInWatchlist": isListingWatchList,
            "allComments": allComments,
            "isOwner":isOwner,
        })


def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']
    newComment = Comments(
        author = currentUser,
        listing=listingData, 
        message=message
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))
def all_listings(request):
    listings = Listing.objects.all()
    return HttpResponse(f"Listings: {listings}")

def displayWatchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    currentUser = request.user 
    listings = currentUser.watching_listings.all().order_by('-id')
    
    # Séparer les annonces actives et fermées
    active_listings = listings.filter(isActive=True)
    closed_listings = listings.filter(isActive=False)
    
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "active_listings": active_listings,
        "closed_listings": closed_listings,
        "total_count": listings.count()
    })

def removeWatchlist(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    try:
        listingData = get_object_or_404(Listing, pk=id)
        currentUser = request.user 
        
        if currentUser in listingData.watchlist.all():
            listingData.watchlist.remove(currentUser)
            
        # Rediriger vers la watchlist si on vient de là, sinon vers le listing
        if 'watchlist' in request.META.get('HTTP_REFERER', ''):
            return HttpResponseRedirect(reverse("watchlist"))
        else:
            return HttpResponseRedirect(reverse("listing", args=(id, )))
            
    except Listing.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))

def addWatchlist(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    try:
        listingData = get_object_or_404(Listing, pk=id)
        currentUser = request.user 
        
        # Vérifier que l'utilisateur n'est pas déjà dans la watchlist
        if currentUser not in listingData.watchlist.all():
            listingData.watchlist.add(currentUser)
            
        return HttpResponseRedirect(reverse("listing", args=(id, )))
        
    except Listing.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    
    # Récupérer les watchlists de l'utilisateur connecté
    user_watchlist_ids = []
    if request.user.is_authenticated:
        user_watchlist_ids = list(request.user.watching_listings.values_list('id', flat=True))
    
    if request.method == "POST":
        try:
            categoryFromForm = request.POST["category"]
            category = Category.objects.get(categoryName=categoryFromForm)
            activeListings = activeListings.filter(category=category)
        except (KeyError, Category.DoesNotExist):
            pass
    
    return render(request, "auctions/index.html", {
        "Listings": activeListings,
        "categories": allCategories,
        "user_watchlist_ids": user_watchlist_ids
    })

def displayCategory(request):
    if request.method == "POST":
        categoryFromForm = request.POST["category"]
        category = Category.objects.get(categoryName=categoryFromForm)
        activeListings = Listing.objects.filter(isActive=True, category=category)
    else:
        activeListings = Listing.objects.filter(isActive=True)
    
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "Listings": activeListings,
        "categories": allCategories
    })
def createListing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"] # 'imageurl' pour correspondre à votre formulaire
        price = request.POST["price"]
        category = request.POST["category"]
        currentUser = request.user
        categoryData = Category.objects.get(categoryName=category)

        bid = Bid(bid=float(price), user=currentUser)
        bid.save()

        newListing = Listing(
            title=title, 
            description=description,
            imageUrl=imageurl, # Assurez-vous que c'est bien 'imageUrl'
            price=bid, # La parenthèse fermante était en trop ici
            category=categoryData,
            owner=currentUser,
        ) # Cette parenthèse fermait la définition de Listing
        newListing.save()
        return HttpResponseRedirect(reverse("index")) # Utilisez le nom de la vue "index"




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
