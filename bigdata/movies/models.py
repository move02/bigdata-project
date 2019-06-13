# from django.db import models
# -*- coding: utf-8 -*-
from djongo import models
from django.conf import settings as djangoSettings
import os,csv
import pymongo
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import datetime
import numpy as np
from sklearn.cluster import KMeans


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

class Club(models.Model):
    name = models.CharField(max_length=200, unique=True)
    desc = models.TextField(default=None)
    recommended = models.ManyToManyField(Movie)

    def __str__(self):
        return self.name

    def has_member(self, user):
        return self.users(manager="object").get(pk=user.pk).exists()

#그룹별 선호도
    def pf_movie():
        numarrDic = {}
        grouppfDic = {}
        groupnum = 200

        for i in range(groupnum):
            tempdic = {}
            numdic = {}
            numdicArr=[]

            print("group : ", i)
            for us in User.objects.filter(club_id=i):

                for rat in Rating.objects.filter(user_id=us.id):
                    if rat.movie_id in tempdic.keys():
                        tempdic[rat.movie_id] = tempdic[rat.movie_id] + rat.rating
                        numdic[rat.movie_id] = numdic[rat.movie_id] + 1
                    else:
                        tempdic[rat.movie_id] = rat.rating
                        numdic[rat.movie_id] = 1

            for key in tempdic.keys():
                tempdic[key] = tempdic[key]/numdic[key]

            #그룹별 영화 평점 평균 정보
            grouppfDic[i] = tempdic
            numarrDic[i] = numdic

        clubBestmv={}

        #최대 평점 영화 구하기
        for gid in grouppfDic.keys():
            #print(gid)
            tempBV = []
            for mvid in grouppfDic[gid].keys(): #영화 id
                if numarrDic[gid][mvid] >= 5 and grouppfDic[gid][mvid] >= 4.0:
                    mv = Movie.objects.get(id=mvid)
                    tempBV.append(mvid)
                elif numarrDic[gid][mvid] >= 2 and grouppfDic[gid][mvid] >= 5:
                    mv = Movie.objects.get(id=mvid)
                    #print(gid, ':', mv.title)
                    tempBV.append(mvid)
            clubBestmv[gid] = tempBV

        #값  확인
        for grid in clubBestmv.keys():
            cl = Club.objects.get(id=grid)
            for mvid2 in clubBestmv[grid]:
                mv = Movie.objects.get(id=mvid2)
                cl.recommended.add(mv)
                #print(grid,' : ',mv.title)
                cl.save()

    
    def has_member(self, user):
        return self.users.filter(id=user.pk).exists()

    def make_prefdata(self):
        import csv,random
        f = open(djangoSettings.STATICFILES_DIRS[0] + '/movies/data/club_{}.csv'.format(self.id), 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        wr.writerow(['movie', 'ratings'])


        total_count = self.users.count()
        ucount = 1
        if total_count > 200:
            sampling = random.sample(range(0,total_count), k=200)
            all_users = self.users.all()
            for ran_num in sampling:
                u = all_users[ran_num]
                print("current user no : " + str(ucount))
                rcount = 1
                for r in u.ratings.all():
                    if rcount > 50:
                        break
                    wr.writerow([r.movie.id, r.rating])
                    rcount += 1
                ucount += 1
        else:
            sampling = self.users.all()
            for u in sampling:
                print("current user no : " + str(ucount))
                rcount = 1
                for r in u.ratings.all():
                    if rcount > 50:
                        break
                    wr.writerow([r.movie.id, r.rating])
                    rcount += 1
                ucount += 1
        

        f.close()

class User(AbstractUser):
    username = None
    name = models.CharField(max_length=200, unique=True)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, default=None, related_name="users")

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name

    def subset( self ):
        return self.id % 29063

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
        
        for k, v in genre_dict.items():
            if len(v) > 0:
                avg = sum(v) / len(v)
                pref = self.preferences(manager="objects").create(genre=k, avg_rating=avg)
                pref.save()

#수정 중
    def signup_club(self):
        umegenList = ['Animation', 'Comedy', 'Family', 'Adventure', 'Fantasy', 'Romance', 'Drama', 'Action', 'Crime',
                   'Thriller', 'Horror', 'History', 'Science Fiction', 'Mystery', 'War', 'Foreign', 'Music',
                   'Docntary', 'Western', 'TV Movie', 'Odyssey Media', 'Pulser Productions', 'Rogue State',
                   'The Cartel']
        pre = [2.0 for _ in range(0, 20)]

        userid = self.id
        pref_queryset = self.preferences.all()
        for prftag in pref_queryset:
            pre[genList.index(prftag.genre)] = prftag.avg_rating

        import joblib
        save_file = djangoSettings.STATICFILES_DIRS[0] + '/movies/clustering.sav'
        kmeans = joblib.load(save_file)

        X2 = np.array(pre)
        print(userid, "의 그룹정보 : ", kmeans.predict(X2.reshape(1, -1))[0])

        #해당 유저의 그룹정보 return
        return kmeans.predict(X2.reshape(1, -1))[0]



    def mk_club():
        genList = ['Animation', 'Comedy', 'Family', 'Adventure', 'Fantasy', 'Romance', 'Drama', 'Action', 'Crime',
                   'Thriller', 'Horror', 'History', 'Science Fiction', 'Mystery', 'War', 'Foreign', 'Music',
                   'Documentary', 'Western', 'TV Movie', 'Odyssey Media', 'Pulser Productions', 'Rogue State',
                   'The Cartel']

        user_prfList = []
        useridList = []
        usergroupDic={}
        userprfDic={}
        knum = 200

        #k수(그룹수)
        clubUserlist = [[] for _ in range(0, knum)]

        #29063
        for userid in range(1, 29063):
            prfList = [2.0 for _ in range(0, 20)]
            for k in PrefTag.objects.filter(user_id=userid):
                prfList[genList.index(k.genre)] = k.avg_rating
            user_prfList.append(prfList)
            useridList.append(userid)
            userprfDic[userid] = prfList

        X = np.array(user_prfList)

        # 클러스터링 하는 부분
        kmeans = KMeans(n_clusters=knum)
        kmeans.fit(X)
        
        # 학습 완료된 모델 저장
        import joblib
        save_file = djangoSettings.STATICFILES_DIRS[0] + '/movies/clustering.sav'
        joblib.dump(kmeans, save_file)

        for i in range(len(useridList)):
            # dic에 id별 그룹 정보 저장
            usergroupDic[useridList[i]] = kmeans.labels_[i]
            clubUserlist[kmeans.labels_[i]].append(useridList[i])

        #그룹이름 - 선호 장르 3개
        groupprfGenreDIc={}
        groupnum = 0
        for oneClubUsers in clubUserlist:
            tempprfs = [0.0 for _ in range(0, 20)]
            cnt = len(oneClubUsers)
            for usr in oneClubUsers:
                #그룹에 있는 유저들의 평점 합
                for i in range(0, len(tempprfs)):
                    tempprfs[i] = tempprfs[i] + userprfDic[usr][i]

            #평균 계산
            for t in range(0, len(tempprfs)):
                tempprfs[t] = tempprfs[t] / cnt

            groupPrfGenre = []
            desc = ""
            for i in range(3):
                prfindex = tempprfs.index(max(tempprfs))
                groupPrfGenre.append(genList[prfindex])
                if i == 2:
                    desc = desc + genList[prfindex]
                else:
                    desc = desc + genList[prfindex] + ', '
                tempprfs[prfindex] = 0

            #클럽 정보 저장
            groupname = 'group' + str(groupnum)
            club, created = Club.objects.update_or_create(id=groupnum, defaults={'name': groupname, 'desc': desc})
            groupprfGenreDIc[groupnum] = groupPrfGenre
            groupnum = groupnum + 1

        #user-club 저장
        for i in range(len(useridList)):
            u = User.objects.get(id=useridList[i])
            u.club_id = Club.objects.get(id=kmeans.labels_[i])
            u.save()






class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, default=None, related_name="posts")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.content

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
