from django.forms.widgets import HiddenInput
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from PIL import Image
from django.forms import ModelForm
from django import forms
from geopy.geocoders import Nominatim
import json
from django.db.models import Avg
import datetime
from django.contrib import messages

from geopy.geocoders.nominatim import _REJECTED_USER_AGENTS


from .models import Rating, User, UserProfile, Ride


# Create your views here.




def index(request):
    return render(request, "carpool/index.html")

# Shows ride as per selection

def rides(request):

    toLocation = request.GET.get("toLocation").split(',')
    fromLocation = request.GET.get("fromLocation").split(',')
    rideSelection = Ride.objects.filter(
        cityFrom=fromLocation[0], cityTo=toLocation[0], completed=False, leavingOn__range=[datetime.date.today(), datetime.date.today()+datetime.timedelta(days=30)]).order_by('leavingOn', 'timeLeaving')
    allRides = Ride.objects.all()

    if rideSelection.count() == 0:
        return render(request, "carpool/index.html", {
            "message": "Unfortunately there are no rides for your selection",
        })

    return render(request, "carpool/rides.html", {
        "rides": rideSelection,
    })

# Shows rides you are a passanger

def myRides(request):

    rates = [1, 2, 3, 4, 5]
    my_rides = Ride.objects.all().order_by('-leavingOn')
    ratedRides = Rating.objects.all()

    return render(request, "carpool/myrides.html", {
        "rides": my_rides,
        'rates': rates,
        'ratedRides': ratedRides,
    })

# Shows rides where you are a driver 

def myRoutes(request):
    my_routes = Ride.objects.all().order_by('-leavingOn')
    return render(request, "carpool/myroutes.html", {
        "rides": my_routes
    })


# Function to delete your ride

def deleteRoute(request, ride_id):
    routeToDelete = Ride.objects.get(id=ride_id)
    if request.method == "POST":
        routeToDelete.delete()
        return HttpResponseRedirect(reverse("myroutes"))

# Function to complete your ride

def completeRoute(request, ride_id):
    routeToComplete = Ride.objects.get(id=ride_id)
    if request.method == "POST":
        routeToComplete.completed = True
        routeToComplete.save()
        return HttpResponseRedirect(reverse("index"))

# Rating funtionality

def rateRide(request):
    if request.method == "POST":
        ride = Ride.objects.get(id=request.POST["thisRideID"])
        rideToRate = Rating()
        rideToRate.rate = request.POST["submit"]
        rideToRate.user = request.user
        rideToRate.driver = ride.driver
        rideToRate.ride = Ride.objects.get(id=request.POST["thisRideID"])
        rideToRate.text = request.POST["rideText"]
        ride.usersRated.add(request.user)
        rideToRate.save()
        messages.success(request, "Your review is saved")
        return HttpResponseRedirect(reverse("myrides"))

# Adding a passanger functionality

def addPassenger(request, ride_id):
    if request.method == "POST":
        ride = Ride.objects.get(id=ride_id)
        if request.user in ride.passangers.all():
            ride.passangers.remove(request.user)
        else:
            ride.passangers.add(request.user)
        return HttpResponseRedirect(reverse("myrides"))

# User profile view

def userProfile(request, user_id):
    ridesCompleted = Ride.objects.filter(driver=user_id, completed=True)
    ridesRated = Rating.objects.filter(driver=user_id)
    avg_rate = list(Rating.objects.filter(
        driver=user_id).aggregate(Avg('rate')).values())[0]
    profile = User.objects.get(id=user_id)
    return render(request, "carpool/profile.html", {
        "profile": profile,
        'ridesCompleted': ridesCompleted,
        'ridesRated': ridesRated,
        'avg_rate': avg_rate
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
            return render(request, "carpool/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "carpool/login.html")


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
            return render(request, "carpool/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)

            if 'profileImage' in request.FILES:
                user.image = request.FILES['profileImage']

            user.save()
        except IntegrityError:
            return render(request, "carpool/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "carpool/register.html")

# Post new ride function

def newride(request):

    geolocator = Nominatim(user_agent="carpool")

    if request.method == "POST":

        ride = Ride()

        fromLocation = request.POST["fromLocation"].split(',')
        toLocation = request.POST["toLocation"].split(',')

        ride.driver = request.user
        ride.leavingOn = request.POST["dateWhen"]
        ride.timeLeaving = request.POST["time"]
        ride.cityFrom = fromLocation[0]
        ride.cityTo = toLocation[0]
        ride.pickUpAddress = request.POST["pickUpLocation"]

        address = request.POST["pickUpLocation"].split(',')

        indices_to_access = [0, 2]
        accessed_mapping = map(address.__getitem__, indices_to_access)
        accessed_list = list(accessed_mapping)

        location = geolocator.geocode(str(accessed_list))

        ride.pickUpLocation = f"{location.latitude},{location.longitude}"

        ride.plateNumber = request.POST["carTag"]
        ride.price = request.POST["price"]
        ride.seats = request.POST["seats"]
        ride.phoneNumber = request.POST["phone"]

        if 'carImage' in request.FILES:
            ride.carImage = request.FILES['carImage']

        ride.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "carpool/newride.html")
