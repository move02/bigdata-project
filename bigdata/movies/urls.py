from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('api/genres_count', views.genres_count, name='genres_count'),

    # path('movies/', include('movies.urls'))
]
