from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
import json

from .models import User, Post, Follow, Like



def index(request):
    allPosts = Post.objects.all().order_by("id").reverse()

    paginator = Paginator(allPosts, 10)
    pageNo = request.GET.get('page')
    postsOfPage = paginator.get_page(pageNo)
    
    allLikes = Like.objects.all()
    
    likedList = []
    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                likedList.append(like.post.id)
    except:
        None

    counter = {}
    for post in allPosts:
        counter[post] = post.likes

    return render(request, "network/index.html", {
        "allPosts" : allPosts,
        "postsOfPage" : postsOfPage,
        "likedList" : likedList,
        "counter" : counter
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
    
def create(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))
    
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    allPosts = Post.objects.filter(user=user).order_by("id").reverse()

    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(user_follower=user)

    try:
        checkFollow = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(checkFollow) != 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False

    paginator = Paginator(allPosts, 10)
    pageNo = request.GET.get('page')
    postsOfPage = paginator.get_page(pageNo)

    allLikes = Like.objects.all()
    
    likedList = []
    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                likedList.append(like.post.id)
    except:
        None

    counter = {}
    for post in allPosts:
        counter[post] = post.likes

    return render(request, "network/profile.html", {
        "allPosts" : allPosts,
        "postsOfPage" : postsOfPage,
        "username" : user.username,
        "following" : following,
        "followers" : followers,
        "isFollowing" : isFollowing,
        "user_profile" : user,
        "likedList" : likedList,
        "counter" : counter
    })

def follow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username = userfollow)

    f = Follow(user=currentUser, user_follower=userfollowData)
    f.save()

    user_id = userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

def unfollow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username = userfollow)

    f = Follow.objects.get(user=currentUser, user_follower=userfollowData)
    f.delete()

    user_id = userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))


def following(request):
    user = User.objects.get(pk=request.user.id)
    following = Follow.objects.filter(user=user)
    allPosts = Post.objects.all().order_by('id').reverse()

    followingPosts =[]

    for post in allPosts:
        for person in following:
            if person.user_follower == post.user:
                followingPosts.append(post)

    paginator = Paginator(followingPosts, 10)
    pageNo = request.GET.get('page')
    postsOfPage = paginator.get_page(pageNo)

    allLikes = Like.objects.all()
    
    likedList = []
    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                likedList.append(like.post.id)
    except:
        None

    counter = {}
    for post in allPosts:
        counter[post] = post.likes

    return render(request, "network/following.html", {
        "postsOfPage" : postsOfPage,
        "likedList" : likedList,
        "counter" : counter
    })

def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        toeditPost = Post.objects.get(pk=post_id)
        toeditPost.content = data["content"]
        toeditPost.save()
        return JsonResponse({"message": "Change Successful", "data": data["content"]})
    
def add_like(request, post_id):
    user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=post_id)
    newLike = Like(user=user, post=post)
    post.likes += 1
    post.save()
    newLike.save()   
    return JsonResponse({"message": "Like Added", "counter": post.likes})

def remove_like(request, post_id):
    user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=post_id)
    if post.likes == 0:
        post.save()
        like = Like.objects.filter(user=user, post=post)
        like.delete()
        return JsonResponse({"message": "Like Removed", "counter": post.likes})
    else:
        post.likes -= 1
        post.save()
        like = Like.objects.filter(user=user, post=post)
        like.delete()
        return JsonResponse({"message": "Like Removed", "counter": post.likes})

