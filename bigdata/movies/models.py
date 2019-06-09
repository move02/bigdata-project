# from django.db import models
from djongo import models
from django.conf import settings as djangoSettings
import os,csv
import pymongo
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import datetime

# Create your models here.

class ProductionCompany(models.Model):
    company_id = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ProductionCountry(models.Model):
    country_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SpokenLanguage(models.Model):
    language_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Genre(models.Model):
    genre_id = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def list_of_genres():
        conn = pymongo.MongoClient('localhost', 27017)

        db = conn.get_database('moviedb')
        collection = db.get_collection('movies_genre')
        genre_list = collection.distinct('name')
        return genre_list

class Collection(models.Model):    
    collection_id = models.IntegerField(default=0)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    movie_id = models.IntegerField()
    imdb_id = models.CharField(blank=True, max_length=200)
    overview = models.CharField(max_length=200)
    popularity = models.FloatField(default=0)
    poster = models.URLField()
    production_companies = models.ManyToManyField(ProductionCompany)
    production_countries = models.ManyToManyField(ProductionCountry)
    release_date = models.DateField()
    revenue = models.IntegerField(default=0)
    runtime = models.IntegerField(default=0)
    spoken_languages = models.ManyToManyField(SpokenLanguage)
    status = models.CharField(max_length=200)
    tagline = models.CharField(max_length=200)
    video = models.BooleanField()
    genres = models.ManyToManyField(Genre)
    vote_avg = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    original_language = models.CharField(max_length=200)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def count_genres(year):
        genres = []
        queryset = Movie.objects.filter(release_date__gte=datetime.date(year, 1, 1),
                                release_date__lte=datetime.date(year+9, 12, 31))
        
        for movie in queryset:
            m_genres = movie.genres(manager='objects').all()
            for genre in m_genres:
                if len(genres) == 0:
                    new_one = {'genre' : genre.name, 'count' : 1}
                    genres.append(new_one)
                    print(genre.name + " Added // genres len : " + str(len(genres)))
                else:
                    length = len(genres)
                    count = 1
                    for g in genres:
                        if genre.name == g['genre']:
                            g['count'] += 1  
                            print(genre.name + " + 1")
                            break
                        elif count == length:
                            new_one = {'genre' : genre.name, 'count' : 1}
                            genres.append(new_one)
                            print(genre.name + " Added // genres len : " + str(len(genres)))
                            break
                        else:
                            count+=1
        import csv    
        f = open(djangoSettings.STATICFILES_DIRS[0] + '/movies/data/genre_{}.csv'.format(year), 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        wr.writerow(['name', 'count'])
        for line in genres:
            newline = [line['genre'], line['count']]
            wr.writerow(newline)
        f.close()
        return
    
class User(AbstractUser):
    username = None
    name = models.CharField(max_length=200, unique=True)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name

    def set_preference_tag(self):
        genre_list = Genre.list_of_genres()
        genre_dict = {}

        for g in genre_list:
            genre_dict[g] = []
        
        for rating in self.ratings(manager="objects").all():
            mov = Movie.objects.get(id=rating.movie_id)
            genres = mov.genres(manager="objects").all()
            for genre in genres:
                genre_dict[genre.name].append(rating.rating)
        
        for k,v in genre_dict.items():
            if len(v) > 0:
                avg = sum(v) / len(v)
                pref = self.preferences(manager="objects").create(genre=k, avg_rating=avg)
                pref.save()


class PrefTag(models.Model):
    genre = models.CharField(max_length=200)
    avg_rating = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="preferences")

    def __str__(self):
        return self.genre + str(self.avg_rating)


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default=None, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="ratings")
    rating = models.FloatField(default=0)

# 그룹에 해당하는 유저 
class group_users(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()
    
# 각 그룹의 정보 (현재는 임의의 이름만 들어가있음)
class group_info(models.Model):
    name = models.CharField(blank=True, max_length=200)
    def __str__(self):
        return self.name
