from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django import forms

from .models import User, Listing, Category, Comment, Bid

class NewListingForm(forms.Form):
    listing_title = forms.CharField(label="", max_length=64, required=True, widget=forms.TextInput(attrs={'placeholder': 'e.g. Harry Potter Wand', 'class': 'form-control form-field'}))
    listing_description = forms.CharField(label="", max_length=500, required=True, widget=forms.Textarea(attrs={'placeholder': 'e.g. This wand is made out of wood, etc.', 'class': 'form-control form-field'}))
    listing_starting_bid = forms.IntegerField(label="", min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control form-field'}))
    listing_image = forms.ImageField(label="")
    
    CHOICELIST = ()

    all_categories = Category.objects.all()
    for category in all_categories:
        CHOICELIST = CHOICELIST + ((category.id, category.category_name),)

    listing_category = forms.ChoiceField(choices=CHOICELIST, required=True, widget=forms.Select(attrs={'class': 'form-control form-field'}))


def index(request):
    listings = Listing.objects.filter(listing_open = 1)

    return render(request, "auctions/index.html", {
        "listings":listings
    })

def view_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    bids = listing.listing_bids.all()
    bids.aggregate(Max('bid_value'))
    highest_bid = bids.order_by('-bid_value').first()

    amount_bids = len(bids)

    watchlisters = listing.listing_watchlist.all()
    
    if request.user in watchlisters:
        watchlist_message = "Remove from watchlist"
    else:
        watchlist_message = "Add to watchlist"

    return render(request, "auctions/view_listing.html", {
        "listing":listing,
        "comments": listing.listing_comments.all(),
        "bids": bids,
        "amount_bids":amount_bids,
        "highest_bid": highest_bid,
        "watchlist_message": watchlist_message
    })


@login_required
def place_bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)

        bid = int(request.POST["bid"])

        listing.listing_current_bid = bid
        listing.save()

        new_bid = Bid(bid_value = bid, bid_user = request.user, bid_listing = listing)
        new_bid.save()
        return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))

@login_required
def place_comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)

        comment = request.POST["comment"]

        new_comment = Comment(comment_content = comment, comment_user = request.user, comment_listing = listing)
        new_comment.save()
        return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))

@login_required
def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing_title = form.cleaned_data["listing_title"]
            listing_description = form.cleaned_data["listing_description"]
            listing_starting_bid = form.cleaned_data["listing_starting_bid"]
            listing_category = Category.objects.get(pk=form.cleaned_data["listing_category"])
            listing_image = form.cleaned_data["listing_image"]

            new_listing = Listing(listing_title = listing_title, listing_description = listing_description, listing_starting_bid = listing_starting_bid, listing_category = listing_category, listing_user = request.user, listing_current_bid = listing_starting_bid, listing_image = listing_image, listing_open = 1)
            new_listing.save()
            return HttpResponseRedirect(reverse("view_listing", args=(new_listing.id,)))
        else:
            return render(request, "auctions/create_listing.html", {
                "form" : form
            })

    return render(request, "auctions/create_listing.html", {
        "form": NewListingForm()
    })

def categories(request):
    categories = Category.objects.all()

    return render(request, "auctions/categories.html", {
        "categories":categories
    })

def view_category(request, category_name):
    category = Category.objects.get(category_name = category_name)
    listings = Listing.objects.filter(listing_category = category)

    return render(request, "auctions/view_category.html", {
        "listings": listings,
        "category_name": category_name,
    })


@login_required
def watchlist(request, user_id):
    user = User.objects.get(pk = user_id)
    listings = Listing.objects.filter(listing_watchlist = user)

    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "user": user
    })

@login_required
def your_listings(request):
    listings = Listing.objects.filter(listing_user = request.user, listing_open = 1)

    return render(request, "auctions/your_listings.html", {
        "listings": listings
    })

@login_required
def your_wins(request):
    closed_listings = Listing.objects.filter(listing_open = 0)

    listings = []

    for listing in closed_listings:
        bids = listing.listing_bids.all()
        bids.aggregate(Max('bid_value'))
        highest_bid = bids.order_by('-bid_value').first()

        if highest_bid.bid_user == request.user:
            listings.append(listing)
    return render(request, "auctions/your_wins.html", {
        "listings": listings
    })


@login_required
def manage_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    watchlisters = listing.listing_watchlist.all()
    
    if request.user in watchlisters:
        listing.listing_watchlist.remove(request.user)
    else:
        listing.listing_watchlist.add(request.user)

    return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))


@login_required
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.listing_open = 0
    listing.save()

    return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))

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
