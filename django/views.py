
from multiprocessing import context
from os import rename
from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Profile, Post, Like, FollowersCount
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

# Create your views here.

@login_required(login_url='signin')
def index(request):
    # for updating profile picture in index page => get object for currently log in user => and use this object to get profile
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user=user_object)

   # user_following_list = []
    #feed = []

    user_following = FollowersCount.objects.filter(follower = request.user.username)

    #for users in user_following:
     #   user_following_list.append(users.user)

    #for usernames in user_following_list:
     #   feed_lists = Post.objects.filter(user=usernames)
      #  feed.append(feed_lists)

    #feed_list = list(chain(*feed))

    # getting all posts from db
#  -------------------------------
    # user suggestions

   # all_users = User.objects.all()

    #user_following_all = []

   # for user in user_following:
    #    user_list = User.objects.get(username=user.user)
     #   user_following_all.append(user_list)

    #new_suggestions_list = []
   # 6af3ad0f-8f76-4ed9-9e77-c8d6bbe051e5
    posts = Post.objects.all()

    context = {'user_profile': user_profile, 'posts': posts}
    return render(request, 'index.html', context)

# ---------------   search -----------------

@login_required(login_url='signin')

def search(request):

    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    

    
    if request.method == "POST":
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains = username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    else:
        redirect("/")
    
    return render(request, 'search.html', { 'user_profile': user_profile, 'username_profile_list': username_profile_list })


#----------------------- upload ---------------

@login_required(login_url='signin')
def upload(request):

    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')   # here image_upload bcz we have given name in index.html line 81
        caption = request.POST['caption']
    
        new_post = Post.objects.create(user = user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect("/")

            
#------------------  like seciton ------------

@login_required(login_url='signin')
def like(request):
    
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    # for checking if user has alredy liked a post  or not 
    like_filter = Like.objects.filter(post_id=post_id, username=username).first()

    # if not liked before
    if like_filter == None:
        new_like = Like.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect('/')        
    
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('/')


# ------------------ profile -------------
@login_required(login_url='signin')

def profile(request, pk):

    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user = user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'

    else:
        button_text = 'Follow'

    user_follower = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_posts_length': user_posts_length,
        'button_text': button_text,
        'user_follower': user_follower,
        'user_following': user_following
    }

    return render(request, 'profile.html', context)

#  --------------  follow -------------

@login_required(login_url='signin')

def follow(request):
    
    if request.method == "POST":
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)

        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)

    else:
        return redirect("/")

#-----------------------  settings -----------------

@login_required(login_url='signin')

def settings(request):
    
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            bio = request.POST['bio']
            location = request.POST['location']
            workingat = request.POST['workingat']

            user_profile.firstname = firstname
            user_profile.lastname = lastname
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.workingat = workingat
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            bio = request.POST['bio']
            location = request.POST['location']
            workingat = request.POST['workingat']


            user_profile.firstname = firstname
            user_profile.lastname = lastname
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.workingat = workingat
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})
            

# --------------------------  signup ----------------


def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = authenticate(username=username, password=password)
                login(request, user_login)
                


                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

# --------------------signin -----------
def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('signin')
    else: 
        return render(request, 'signin.html')

@login_required(login_url='signin')
def log_out(request):
    logout(request)
    return redirect('signin')