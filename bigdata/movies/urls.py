from django.urls import path, include
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('group_list', views.group_list, name='group_list'),
    path('group_view', views.group_view, name='group_view'),
    path('login_register', views.login_register, name='login_register'),
    path('api/genres_count/<int:year>', views.genres_count, name='genres_count'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
] 
urlpatterns+=[
    path('', include('django.contrib.auth.urls')),
]