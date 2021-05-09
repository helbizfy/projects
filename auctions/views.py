from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from .models import Listing, Watchlist, Comment, Bid
from django.contrib import messages

from .models import User


class NewListing(forms.Form):
    title = forms.CharField(label='Listing Title', widget=forms.TextInput(
        attrs={'class': 'form-control col-md-8 col-lg-8'}))
    description = forms.CharField(label='Listing Description', widget=forms.Textarea(
        attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10}))
    listing_picture = forms.ImageField(label='Listing Image')
    starting_bid = forms.IntegerField(label='Starting Bid')
    category = forms.CharField(label='Category')


class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

        labels = {
            'body': ''
        }

        widgets = {

            'body': forms.Textarea(
                attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 8}),

        }


class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid',
                  'category', 'listing_picture']

        labels = {
            'starting_bid': 'Starting bid $'
        }

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control col-md-8 col-lg-8'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 8}),
            'starting_bid': forms.NumberInput(
                attrs={'class': 'form-control col-md-1 col-lg-1'}),
            'category': forms.TextInput(
                attrs={'class': 'form-control col-md-3 col-lg-3'}),
            'listing_picture': forms.URLInput(
                attrs={'class': 'form-control col-md-3 col-lg-3', 'placeholder': 'Image link'}),
        }


class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

        labels = {
            'bid': 'Your Bid'
        }

        widgets = {

            'bid': forms.NumberInput(
                attrs={'class': 'form-control col-md-6 col-lg-6'})

        }


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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


def newListing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            form.instance.author = User.objects.get(
                username=request.user.username)
            form.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/newListing.html", {
            "form": NewListingForm()
        })


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": NewCommentForm(),
        "bid_form": NewBidForm()

    })


def category(request, cat_type):
    return render(request, "auctions/category.html", {
        "listings": Listing.objects.filter(category=cat_type),
        "cat": cat_type
    })


def category_list(request):
    categories = Listing.objects.values('category').distinct()
    return render(request, "auctions/category_list.html", {
        "listings": categories
    })


def watchlist(request, listing_id):
    if request.method == 'POST':
        item = Listing.objects.get(id=listing_id)
        existing = Watchlist.objects.filter(
            user=request.user.username, listing=listing_id)
        if existing:
            return render(request, "auctions/listing.html", {
                "listing": item,
                "not_added": "This item is on your watchlist",
                "bid_form": NewBidForm(),
                "form": NewCommentForm()
            })
        else:
            watchlist, created = Watchlist.objects.get_or_create(
                user=request.user.username)
            watchlist.listing.add(item)
            return render(request, "auctions/listing.html", {
                "listing": item,
                "added": "Listing added to your watchlist",
                "bid_form": NewBidForm(),
                "form": NewCommentForm()
            })


def watchlist_list(request):
    existing = Watchlist.objects.filter(user=request.user.username)
    if existing:
        user = Watchlist.objects.get(user=request.user.username)
        user_watchlist = user.listing.all()
        return render(request, "auctions/watchlist_list.html", {
            "listings": user_watchlist
        })
    else:
        return render(request, "auctions/watchlist_list.html")


def delete_watchlist_item(request, listing_id):
    if request.method == 'POST':
        user = Watchlist.objects.get(user=request.user.username)
        item_to_delete = user.listing.get(id=listing_id)
        user.listing.remove(item_to_delete)
        return HttpResponseRedirect(reverse("watchlist_list"))


def newComment(request, listing_id):
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user.username
            form.instance.listing = Listing.objects.get(id=listing_id)
            form.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def newBid(request, listing_id):
    if request.method == "POST":
        if Bid.objects.filter(listing=listing_id):
            form = NewBidForm(
                request.POST, instance=Bid.objects.get(listing=listing_id))
            if form.is_valid():
                if form.cleaned_data.get("bid") <= Listing.objects.get(id=listing_id).starting_bid or form.cleaned_data.get("bid") <= Bid.objects.get(listing=listing_id).bid:
                    return render(request, "auctions/listing.html", {
                        "listing": Listing.objects.get(id=listing_id),
                        "message": "Bid is too small",
                        "bid_form": NewBidForm(),
                        "form": NewCommentForm()
                    })
                else:
                    form.instance.user = request.user.username
                    form.save()
        else:
            form = NewBidForm(request.POST)
            if form.is_valid():
                if form.cleaned_data.get("bid") >= Listing.objects.get(id=listing_id).starting_bid:
                    form.instance.user = request.user.username
                    form.instance.listing = Listing.objects.get(id=listing_id)
                    form.save()
                else:
                    return render(request, "auctions/listing.html", {
                        "listing": Listing.objects.get(id=listing_id),
                        "message": "Bid is too small",
                        "bid_form": NewBidForm(),
                        "form": NewCommentForm()
                    })
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(id=listing_id),
            "message": "Your bid is placed",
            "bid_form": NewBidForm(),
            "form": NewCommentForm()
        })


def closeBid(request, listing_id):
    if request.method == "POST":
        obj = Bid.objects.get(listing=listing_id)
        bid_winner = User.objects.get(username=obj.user)

        obj2 = Listing.objects.get(id=listing_id)
        obj2.winner = bid_winner
        obj2.save()
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(id=listing_id),
            "message": f"Auctions is closed and winner is {bid_winner}",
            "bid_form": NewBidForm(),
            "form": NewCommentForm()
        })
