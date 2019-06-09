from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import datetime, pymongo, json
from .models import Movie, Genre
from django.db import connections
from django.db.models import Count
import mimetypes
from django.contrib.auth import login, authenticate, logout
from bigdata import settings
from django.contrib.auth.decorators import login_required

def index(request):
    movies = Movie.objects.filter(release_date__gte=datetime.date(2017,5,1)) 
    return render(request, 'movies/index.html',{
        'movies' : movies
    })

def genres_count(request, year):
    filename = settings.STATICFILES_DIRS[0] + '/movies/data/genre_{}.csv'.format(year)
    fsock = open(filename,"rb")
    return HttpResponse(fsock, content_type=mimetypes.guess_type(filename)[0]) 

def login_register(request):      
    if not request.user.is_authenticated:
        return render(request, 'login-register.html')
    else:
        return redirect(reverse('movies:index'))

def signin(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(name = name, password = password)
        response_data = {}           
        if user is not None:
            login(request, user)                                                                                       
            response_data['result'] = 'Success'
            response_data['message'] = 'You"re logged in'
        else:                                                          
            response_data['result'] = 'Failed'
            response_data['message'] = '로그인 실패. 다시 시도 해보세요.'
        
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return render(request, 'login-register.html')

def signout(request):
    logout(request)
    return redirect('/movies/')
