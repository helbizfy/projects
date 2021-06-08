
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following/<int:page>", views.following, name="following"),
    path("following", views.followingPage, name="followingPage"),

    path("posts/<int:post_id>", views.posts, name="post"),
    path("postsPage/<int:page>", views.post_list_by_page, name="postsPage"),
    path("newpost", views.newPost, name="newpost"),
    path("posts", views.post_list, name="postList"),
    path("newlike/<int:post_id>", views.newLike, name="newlike"),
    path("fallowers/<int:user_id>", views.fallowers, name="fallowers")
]
