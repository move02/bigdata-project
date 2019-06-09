from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index),
    path('login', views.login, name='login'),
    path('api/genres_count/<int:year>', views.genres_count, name='genres_count'),
    path('loginActive', views.genres_count, name='loginActive'),

    # path('movies/', include('movies.urls'))
]
