
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Songs, Artist
from django.conf import settings
import os
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from .models import CustomUser

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        if password == confirm_password:
            user = CustomUser.objects.create_user(username=username, password=password)
            user.name = name
            user.save()
            return redirect('login')
        else:
            # Handle password mismatch error
            pass
    return render(request, 'music/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            # Handle invalid login
            pass
    return render(request, 'music/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')



def home(request):
    username = request.user.name if request.user.is_authenticated else None

    telugu_songs = Songs.objects.filter(language='Telugu')
    hindi_songs = Songs.objects.filter(language='Hindi')
    tamil_songs = Songs.objects.filter(language='Tamil')
    english_songs = Songs.objects.filter(language='English')
    artists = Artist.objects.all()  # Fetch all artists


    context = {
        'telugu_songs': telugu_songs,
        'hindi_songs': hindi_songs,
        'tamil_songs': tamil_songs,
        'english_songs': english_songs,
        'username': username,
        'artists': artists,  # Include artists in the context

    }

    return render(request, 'music/home.html', context)

def artists(request, artist_id):
    artist = Artist.objects.get(pk=artist_id)
    songs = Songs.objects.filter(artist=artist)
    context = {
        'artist': artist,
        'songs': songs,  # Pass the artist's songs to the template
    }
    return render(request, 'music/artists.html', context)



def base(request):
    return render(request, 'music/base.html')

def all_songs(request):
    songs = Songs.objects.all()
    media_url = settings.MEDIA_URL
    songs_with_images = []
    for song in songs:
        # Assuming each song has an image field named 'image'
        if song.image:
            # Constructing the image URL
            image_url = os.path.join(media_url, str(song.image))
            songs_with_images.append((song, image_url))
    return render(request, 'music/all_songs.html', {'songs_with_images': songs_with_images})

def artist_detail(request, artist_id):
    artist = Artist.objects.get(pk=artist_id)
    context = {
        'artist': artist,
    }
    return render(request, 'music/artists.html', context)
def new_songs(request):
    new_songs = Songs.objects.filter(is_new=True)
    return render(request, 'music/new_songs.html', {'new_songs': new_songs})
def old_songs(request):
    old_songs = Songs.objects.filter(is_new=False)
    return render(request, 'music/old_songs.html', {'old_songs': old_songs})
def trending_songs(request):
    trending_songs = Songs.objects.filter(is_trending=True)
    return render(request, 'music/trending_songs.html', {'trending_songs': trending_songs})


def index(request):
    return render(request, 'music/index.html')
def search_view(request):
    # Your search logic here
    return render(request, 'music/search.html')
def display_favorite_songs(request):
    user = request.user
    favorite_songs = user.favorite_songs.all()
    return render(request, 'music/favorite_songs.html', {'favorite_songs': favorite_songs})
