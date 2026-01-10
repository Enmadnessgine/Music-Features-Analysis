from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AudioFile(models.Model):
    file = models.FileField(upload_to="audio/")
    file_hash = models.CharField(max_length=64, unique=True)
    size = models.BigIntegerField()

class Song(models.Model):
    track_id = models.TextField()
    title = models.CharField(max_length=40, default="")
    artist = models.CharField(max_length=40, default="")
    audio = models.ForeignKey(
		AudioFile,
		on_delete=models.PROTECT,
		related_name="songs"
	)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="songs")
    
    class Meta:
        unique_together = ('user', 'audio')
    
class Features(models.Model):
    audio = models.OneToOneField(
		AudioFile,
		on_delete=models.CASCADE,
		related_name="features"
	)
    acousticness = models.FloatField()
    danceability = models.FloatField()
    energy = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    speechiness = models.FloatField()
    tempo = models.FloatField()
    valence = models.FloatField()


class SpotifyToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=300)
    refresh_token = models.CharField(max_length=300)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() >= self.expires_at