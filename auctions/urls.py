from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.newListing, name="newListing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("category/<str:cat_type>", views.category, name="category"),
    path("category", views.category_list, name="category_list"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("watchlist", views.watchlist_list, name="watchlist_list"),
    path("delete_watchlist_item/<int:listing_id>", views.delete_watchlist_item,
         name="delete_watchlist_item"),
    path("newcomment/<int:listing_id>", views.newComment, name="newComment"),
    path("newbid/<int:listing_id>", views.newBid, name="newBid"),
    path("closebid/<int:listing_id>", views.closeBid, name="closeBid")

]
