from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
import json
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime


from .models import User, posts, PostLikes, userFollowing
from .forms import postForm


def index(request):
    return HttpResponseRedirect(reverse("all_posts"))


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def all_posts(request):
    if request.method == "POST":
        form = postForm(request.POST)
        if form.is_valid():
            user = request.user
            content = form.cleaned_data.get("content")
            created_at = datetime.now()
            post_object = posts(created_by=user, content=content, created_at=created_at)
            post_object.save()
            return HttpResponseRedirect(reverse("index"))
    all_posts = posts.objects.all().order_by("-created_at")
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "network/all_posts.html", {"page_obj": page_obj, "form": postForm()}
    )


def profile(request, username):
    user = User.objects.get(username=username)
    user_posts = posts.objects.filter(created_by=user).order_by("-created_at")
    is_current_user = request.user == user
    followers = userFollowing.objects.filter(following=user.id).count()
    is_following = userFollowing.objects.filter(
        follower=request.user.id, following=user.id
    ).count()
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/profile.html",
        {
            "user": user,
            "posts": user_posts,
            "is_current_user": is_current_user,
            "page_obj": page_obj,
            "followers": followers,
            "is_following": is_following,
        }
    )

def following(request):
    user = request.user
    following = userFollowing.objects.filter(follower=user).values('following_id')
    following_posts = posts.objects.filter(created_by__in=following).order_by('-created_at')
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

# API Calls
@csrf_exempt
def like(request, post_id):
    user = request.user
    post = posts.objects.get(id=post_id)

    if request.method == "GET":
        try:
            like_object = PostLikes.objects.get(user=user, post=post)
            like_object.delete()
            post.likes = PostLikes.objects.filter(post=post).count()
        except PostLikes.DoesNotExist:
            like_object = PostLikes(user=user, post=post)
            like_object.save()
            post.likes = PostLikes.objects.filter(post=post).count()
        return JsonResponse(post.serialize())


@csrf_exempt
def follow(request, user_id):
    if request.method == "POST":
        following = User.objects.get(id=user_id)
        try:
            following_user = userFollowing.objects.get(
                follower=request.user, following=following
            )
            following_user.delete()
            followers = userFollowing.objects.filter(
                following=following
            ).count()
            return JsonResponse({"followers": followers})
        except userFollowing.DoesNotExist:
            following_user = userFollowing(
                follower=request.user, following=following
            )
            following_user.save()
            followers = userFollowing.objects.filter(
                following=following
            ).count()
            return JsonResponse({"followers": followers})


@csrf_exempt
def edit(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        post = posts.objects.get(id=post_id)
        post.content = data.get("content")
        post.save()
        return JsonResponse({"content": post.content})
