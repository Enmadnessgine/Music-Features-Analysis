from django.urls import path
from .views import audio_views, profile_views, main_views, search_views, spotify_views, user_views

urlpatterns = [
    path("", main_views.index, name="index"),
    path('signin/', user_views.signin, name = 'signin'),
    path('login/', user_views.user_login, name = 'login'),
    path('logout/', user_views.user_logout, name = 'logout'),
    path("upload/", audio_views.analize_audio, name="upload_audio"),
    path("search/", search_views.load_search, name="search"),
    path("search_ajax/", search_views.search_ajax, name="search_ajax"),
    path("profile/", profile_views.profile, name="profile"),
    path("profile/top_songs/", profile_views.load_ts, name="load_ts"),
    path("profile/stats/", profile_views.load_stats, name="load_stats"),
    path("login/spotify/", spotify_views.spotify_login, name="spotify_login"),
    path("callback/spotify/", spotify_views.spotify_callback, name="spotify_callback"),
    path("load_analizer_info/", profile_views.load_analizer_info, name="load_analizer_info"),
]