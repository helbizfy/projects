from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User, Post, Fallower
from django.forms import ModelForm
from django import forms
import datetime
from django.core.paginator import Paginator


class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body']

        labels = {
            'body': 'New Post'
        }

        widgets = {

            'body': forms.Textarea(
                attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 4}),

        }


def index(request):
    # Pagination settings
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(2)
    return render(request, "network/index.html", {
        "form": NewPostForm(),
        'posts': paginator
    })


@login_required
def followingPage(request):
    # Pagination setting + filter only posts by authors you follow
    followingList = Fallower.objects.get(user=request.user)

    followingpPosts = Post.objects.filter(
        author__in=followingList.fallowing.all())

    followingPaginator = Paginator(followingpPosts, 10)

    return render(request, "network/following.html", {
        'fposts': followingPaginator
    })


@csrf_exempt
@login_required
def following(request, page):
    followingList = Fallower.objects.get(user=request.user)

    posts = Post.objects.filter(
        author__in=followingList.fallowing.all()).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)

    # Return post contents
    if request.method == "GET":
        return JsonResponse([post.serialize() for post in page_obj], safe=False)


def following_list(request):
    followingList = Fallower.objects.get(user=request.user)

    posts = Post.objects.filter(
        author__in=followingList.fallowing.all()).order_by("-timestamp")

    # Return post contents
    if request.method == "GET":
        return JsonResponse([post.serialize() for post in posts], safe=False)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def post_list(request):
    # Query for requested post
    try:
        posts = Post.objects.all().order_by("-timestamp")
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse([post.serialize() for post in posts], safe=False)


def post_list_by_page(request, page):
    # Query for requested posts page
    try:
        posts = Post.objects.all().order_by("-timestamp")
        paginator = Paginator(posts, 10)
        page_obj = paginator.get_page(page)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse([post.serialize() for post in page_obj], safe=False)


@csrf_exempt
@login_required
def fallowers(request, user_id):

    # Return followers
    if request.method == "GET":
        fallowers = Fallower.objects.get(user=user_id)
        return JsonResponse(fallowers.serialize())

    if request.method == 'POST':
        # Fallowing/Unfallow functionality
        user_1, created = Fallower.objects.get_or_create(user=request.user)
        user_2, created = Fallower.objects.get_or_create(user=user_id)
        if user_1.fallowing.filter(id=user_id).exists():
            user_1.fallowing.remove(user_id)
        else:
            user_1.fallowing.add(user_id)

        if user_2.fallowers.filter(username=request.user.username).exists():
            user_2.fallowers.remove(request.user)
        else:
            user_2.fallowers.add(request.user)

    return HttpResponseRedirect(reverse('fallowers', args=(user_id,)))


@csrf_exempt
@login_required
def newPost(request):
    # New post functionality
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            form.instance.author = User.objects.get(
                username=request.user.username)
            form.save()
            return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def posts(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Edit post functionality
    if request.method == "POST":
        data = json.loads(request.body)
        editValue = data.get("newValue")
        post = Post.objects.get(id=post_id)
        post.body = editValue
        post.timestamp = datetime.datetime.now()
        post.save()
        return HttpResponseRedirect(reverse("index"))


@csrf_exempt
@login_required
def newLike(request, post_id):
    # Like button functionality
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
            post.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            post.liked_by.add(request.user)
            post.save()
            return HttpResponseRedirect(reverse("index"))
