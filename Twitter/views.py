from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from Twitter.forms import *
from django.contrib.auth import login, authenticate, logout
from Twitter.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    if request.user.is_authenticated:
        return redirect('/feed/')
    else:
        if request.method == 'POST':
            if 'signupform' in request.POST:
                signupform = SignupForm(data=request.POST)
                signinform = SigninForm()

                if signupform.is_valid():
                    username = signupform.cleaned_data['username']
                    password = signupform.cleaned_data['password1']
                    account = signupform.save()
                    Profile.objects.create(user=account)
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect('/')
            else:
                signinform = SigninForm(data=request.POST)
                signupform = SignupForm()

                if signinform.is_valid():
                    username = signinform.cleaned_data['username']
                    password = signinform.cleaned_data['password']
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                    return redirect('/')

                else:
                    data = request.data_object
                    data.authorized = False
                    data.save()

        else:
            signupform = SignupForm()
            signinform = SigninForm()

        return render(request, 'index.html', {'signupform': signupform, 'signinform': signinform})


@login_required
def signout(request):
    log = LoggedInUser.objects.get(user=request.user)
    log.delete()
    logout(request)
    return redirect('/')


def profile(request, username):
    if request.user.is_authenticated:
        user = User.objects.get(username=username)
        follow_all = Follow.objects.all()
        follows = Follow.objects.filter(user=user)
        followers = Follow.objects.filter(target=user)
        try:
            followers.filter(user=request.user)
            user_follows = True
        except:
            user_follows = False
        print(user_follows)
        tweets = Tweet.objects.filter(user=user).order_by('-created_at')
        if request.method == 'POST':
            form = TweetForm(data=request.POST)

            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()

                redirecturl = request.POST.get('redirect', '/')

                return redirect(redirecturl)
        else:
            form = TweetForm()

        return render(request, 'profile.html', {'form': form, 'user': user, 'followers': followers, 'follows': follows, 'user_follows': user_follows, 'tweets': tweets})
    else:
        return redirect('/')


def feed(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        follow_all = Follow.objects.all()
        follows = Follow.objects.filter(user=user)
        followers = Follow.objects.filter(target=user)
        tweets = Tweet.objects.all().order_by('-created_at')
        user_tweets_count = sum(1 for e in filter(lambda x: x.user == user, tweets))
        if request.method == 'POST':
            form = TweetForm(data=request.POST)

            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()

                redirecturl = request.POST.get('redirect', '/')

                return redirect(redirecturl)
        else:
            form = TweetForm()

        return render(request, 'feed.html', {'form': form, 'user': user, 'followers': followers, 'follows': follows,
                                             'tweets': tweets, 'user_tweets_count': user_tweets_count})
    else:
        return redirect('/')


def follows(request, username):
    user = User.objects.get(username=username)
    profiles = Follow.objects.filter(user=user)
    return render(request, 'users.html', {'title': 'Following', 'profiles': profiles, 'following': True})


def followers(request, username):
    user = User.objects.get(username=username)
    profiles = Follow.objects.filter(target=user)
    return render(request, 'users.html', {'title': 'Followers', 'profiles': profiles, 'following': False})


@login_required
def follow(request, username):
    user = User.objects.get(username=username)
    Follow.objects.create(user=request.user, target=user)
    return redirect('/' + user.username + '/')


@login_required
def stopfollow(request, username):
    user = User.objects.get(username=username)
    follow_obj = Follow.objects.filter(user=request.user, target=user)
    follow_obj.delete()
    return redirect('/' + user.username + '/')


@login_required
def edit_profile(request):
    user = User.objects.get(username=request.user.username)
    profile = user.profile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/' + request.user.username + '/')
    else:
        form = EditProfileForm(initial={'bio': profile.bio, 'birthday': profile.birthday})
    return render(request, 'edit_profile.html', {'form': form, 'user': user})


@login_required
def get_token_v2(request, username):
    user = User.objects.get(username=username)
    token, created = Token.objects.get_or_create(user=user)
    data = {
        "authentication_key": token.authentication_key
    }
    return JsonResponse(data)


@csrf_exempt
def tweet_by_token(request):
    try:
        body = json.loads(request.body)
        authentication_key = body["authentication_key"]
        tweet_title = body["tweet_title"]
        tweet_text = body["tweet_text"]
    except KeyError:
        response = {"status": "Key Not Found"}
        return JsonResponse(response)
    try:
        user_entry = Token.objects.get(authentication_key=authentication_key)
        user = user_entry.user
        Tweet.objects.create(user=user, title=tweet_title, text=tweet_text)
        response = {"status": "OK"}
        return JsonResponse(response)
    except ValidationError:
        response = {"status": "Validation Error"}
        return JsonResponse(response)
