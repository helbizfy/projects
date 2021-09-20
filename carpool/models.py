from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from PIL import Image
from django.conf import settings
import os
from location_field.models.plain import PlainLocationField


class User(AbstractUser):
    image = models.ImageField(null=True, blank=True,
                              default='default.jpg', upload_to='profile_pics')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    image = models.ImageField(null=True, blank=True,
                              default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.name} Profile"


class Ride(models.Model):
    driver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="driver")
    leavingOn = models.DateField()
    timeLeaving = models.TimeField()
    cityFrom = models.CharField(max_length=255, default='Marocco')
    cityTo = models.CharField(max_length=255, default='Marocco')
    pickUpAddress = models.CharField(max_length=255)
    plateNumber = models.CharField(max_length=15)
    city = models.CharField(max_length=255, default='Marocco')
    pickUpLocation = PlainLocationField(based_fields=['pickUpAddress'])
    carImage = models.ImageField(null=True, blank=True,
                                 default='default-car.png', upload_to='car_images')
    price = models.FloatField(default=0)
    passangers = models.ManyToManyField(User, null=True, blank=True)
    seats = models.IntegerField(default=5)
    phoneNumber = models.CharField(max_length=15, default="+371 26179999")
    completed = models.BooleanField(default=False)
    usersRated = models.ManyToManyField(
        User, related_name="usersRated", null=True, blank=True)

    def __str__(self):
        return f"{self.cityFrom} to {self.cityTo} Ride by {self.driver} "


RATE_CHOICES = [
    (1, 'Very bad'),
    (2, 'Bad'),
    (3, 'Good'),
    (4, 'Very nice'),
    (5, 'Excellent'),
]


class Rating(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="rated_by", null=True)
    driver = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="driven_by", null=True)
    ride = models.ForeignKey(
        "Ride", on_delete=models.CASCADE, related_name="ratedRide", null=True)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=255, blank=True, null=True)
    rate = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.ride}  {self.date} "
