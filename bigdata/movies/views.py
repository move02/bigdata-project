from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
import datetime, pymongo, json
from .models import Movie, Genre
from django.db import connections
from django.db.models import Count
import mimetypes

# from .forms import PostForm, CommentForm

def index(request):
    movies = Movie.objects.filter(release_date__gte=datetime.date(2017,5,1)) 
    return render(request, 'movies/index.html',{
        'movies' : movies
    })

def genres_count(request):
    filename = '/Users/move0/dev/django/bigdata/bigdata/static/movies/data/recent_genre.csv'
    fsock = open(filename,"rb")
    return HttpResponse(fsock, content_type=mimetypes.guess_type(filename)[0]) 