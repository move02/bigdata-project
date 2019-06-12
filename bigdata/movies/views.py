from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import datetime, pymongo, json
from .models import Movie, Genre, User, Club, Post, Comment
from django.db import connections
from django.db.models import Count
import mimetypes
from django.contrib.auth import login, authenticate, logout
from bigdata import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    movies = Movie.objects.filter(release_date__gte=datetime.date(2017,5,1))
    usercount = User.objects.all().count
    clubcount = Club.objects.all().count
    posts = Post.objects.all()
    moviecount = Movie.objects.all().count
    return render(request, 'movies/index.html',{
        'movies' : movies,
        'moviecount' : moviecount,
        'usercount' : usercount,
        'clubcount' : clubcount,
        'posts' : posts,
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

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(name = name, password = password)

        response_data = {}
        if user is None:
            user = User.objects.create_user(name = name, password = password, email=email)
            login(request, user)                                                                                       
            response_data['result'] = 'Success'
            response_data['message'] = 'You"re logged in'
        else:                                                          
            response_data['result'] = 'Failed'
            response_data['message'] = '이미 존재하는 Name 임.'
        
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return render(request, 'login-register.html')

def clublist(request):
    clubs = Club.objects.all()
    return render(request, 'club/clublist.html',{
        'clubs' : clubs
    })    

def clubview(request):
    getclubid = request.GET['id']
    currentuser = get_object_or_404(User,id=request.user.id)
    resultclub = Club.objects.filter(id=getclubid)
    usercount = User.objects.filter(club_id=getclubid).count
    ismember = get_object_or_404(Club, id=getclubid).has_member(currentuser)
    clubposts =  Post.objects.filter(club_id=getclubid) 
    postids = [];   
    for clubpost in clubposts:
        postids.append(clubpost.id)
    clubcomments = Comment.objects.filter(post_id__in=postids)
    print(clubcomments)
    #testpost = Post.objects.get(id=1)
    #Comment.objects.create(content="testcomment",post=testpost,author=currentuser)
    return render(request, 'club/clubview.html',{
        'club' : resultclub,
        'usercount' : usercount,
        'ismember' : ismember,
        'clubposts' : clubposts,
        'clubcomments' : clubcomments
    })    

def postsubmit(request):
    if request.method == "POST":
        inputtext = request.POST['inputtext']
        authorid = request.POST['authorid']
        clubid = request.POST['clubid']
        Post.objects.create(content=inputtext,title="test",club_id=clubid,author_id=authorid)
        print(inputtext,authorid,clubid)
        response_data = {}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse(json.dumps(response_data), content_type="application/json")

def commentsubmit(request):
    if request.method == "POST":
        postid = request.POST['post_id']
        authorid = request.POST['author_id']
        icontent = request.POST['content']
        Comment.objects.create(content=icontent, author_id=authorid, post_id=postid)
        response_data = {}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse(json.dumps(response_data), content_type="application/json")

def myclub(request):    
    currentuser = User.objects.filter(id=request.user.id)
    #print(currentuser.club)
    response_data = {}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def clubmember(request): 
    getclubid = request.GET['id']
    resultmembers = User.objects.filter(club_id=getclubid)
    resultclub = Club.objects.filter(id=getclubid)
    usercount = User.objects.filter(club_id=getclubid).count
    print(resultmembers)
    return render(request, 'club/clubmember.html',{
        'club' : resultclub,
        'usercount' : usercount,
        'members':resultmembers
    })

def movielist(request):
    movies = Movie.objects.all().order_by('-release_date')
    moviecount = movies.count
    page = request.GET.get('page', 1)
    paginator = Paginator(movies, 18)
    try:
        currentmovies = paginator.page(page)
    except PageNotAnInteger:
        currentmovies = paginator.page(1)
    except EmptyPage:
        currentmovies = paginator.page(paginator.num_pages)

    return render(request, 'movies/movielist.html', { 
        'movies': currentmovies,
        'moviecount' : moviecount
    })

def movieview(request):
    getmovieid = request.GET['id']
    prarmmovie = Movie.objects.filter(id=getmovieid)
    return render(request, 'movies/movieview.html', { 
        'movie' : prarmmovie
    })

def toprated(request):
    movies = Movie.objects.order_by('-vote_count','-vote_avg')
    moviecount = movies.count
    page = request.GET.get('page', 1)
    paginator = Paginator(movies, 18)
    try:
        currentmovies = paginator.page(page)
    except PageNotAnInteger:
        currentmovies = paginator.page(1)
    except EmptyPage:
        currentmovies = paginator.page(paginator.num_pages)

    return render(request, 'movies/toprated.html', { 
        'movies': currentmovies,
        'moviecount' : moviecount
    })