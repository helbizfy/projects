from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newride", views.newride, name="newride"),
    path("rides", views.rides, name="rides"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addPassenger/<int:ride_id>", views.addPassenger, name="addPassenger"),
    path("myrides", views.myRides, name="myrides"),
    path("myroutes", views.myRoutes, name="myroutes"),
    path("delete/<int:ride_id>", views.deleteRoute, name="deleteRoute"),
    path("completed/<int:ride_id>", views.completeRoute, name="completeRoute"),
    path("rateRide", views.rateRide, name="rateRide"),
    path("profile/<int:user_id>", views.userProfile, name="userProfile")
]
