from django.contrib import admin
from .models import Rating, Ride, User, UserProfile

# Register your models here.

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Ride)
admin.site.register(Rating)
