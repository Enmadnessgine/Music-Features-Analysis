from django.urls import path, include
from . import views, song_views

urlpatterns = [
    path("", views.index, name="index"),
    path('signin/', views.signin, name = 'signin'),
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path("upload/", song_views.analize_audio, name="upload_audio"),
    path("search/", song_views.load_search, name="search"),
    path("search_ajax/", song_views.search_ajax, name="search_ajax"),
    path("profile/", views.profile, name="profile"),
    path("profile/top_songs/", views.load_ts, name="load_ts"),
    path("login/spotify/", views.spotify_login, name="spotify_login"),
    path("callback/spotify/", views.spotify_callback, name="spotify_callback"),
]