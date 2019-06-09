from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
import datetime, pymongo, json
from .models import Movie, Genre
from django.db import connections
from django.db.models import Count
import mimetypes
from django.contrib.auth import login, authenticate
from bigdata import settings


def index(request):
    movies = Movie.objects.filter(release_date__gte=datetime.date(2017,5,1)) 
    return render(request, 'movies/index.html',{
        'movies' : movies
    })

def genres_count(request, year):
    filename = settings.STATICFILES_DIRS[0] + '/movies/data/genre_{}.csv'.format(year)
    fsock = open(filename,"rb")
    return HttpResponse(fsock, content_type=mimetypes.guess_type(filename)[0]) 

def login(request):        
    return render(request, 'login-register.html')

def signin(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(name = name, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        return render(request, 'login-register.html')
