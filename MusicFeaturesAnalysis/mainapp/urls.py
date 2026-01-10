from django.urls import path
from . import views, song_views


urlpatterns = [
    path("", views.index, name="index"),
    path('signin/', views.signin, name = 'signin'),
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path("profile/", views.profile, name="profile"),
    path("upload/", song_views.analize_audio, name="upload_audio"),
]