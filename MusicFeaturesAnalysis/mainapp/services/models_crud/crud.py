from ..model_db import ModelData
from mainapp.models import Song, SearchInfo, SpotifyToken, AudioFile, Features, Statistics

class Audio_(ModelData):
	def __init__(self, model=AudioFile):
		super().__init__(model)
	
	def create_audio(self, file_hash, file, size = None):
		audio, created = self.get_or_create(
			kwargs={"file_hash": file_hash},
			defaults={
				"file": file,
				"size": file.size if size is None else size,
			},
		)

		return audio, created

class Song_(ModelData):
	def __init__(self, model=Song):
		super().__init__(model)
  
	def create_song(self, user, audio, title, artist, track_id = None):
		song, _ = self.get_or_create(
			kwargs={
				"user": user,
				"audio": audio,
			},
			defaults={
				"track_id": track_id or "",
				"title": title,
				"artist": artist,
			},
		)

		return song, _

	def delete(self, user, song_id):
		return super().delete(id=song_id, user=user) > 0

	def get_all(self, user):
		songs = super().get_all(filters={"user": user}, select_related=["audio", "audio__features"])
		return songs

class Features_(ModelData):
	def __init__(self, model=Features):
		super().__init__(model)
	
	def create_features(self, audio, features_data):
		return self.get_or_update(
            kwargs={"audio": audio}, defaults=features_data
        )

class SpotifyToken_(ModelData):	
	def __init__(self, model=SpotifyToken):
		super().__init__(model)
	
	def create_or_update(self, user, access_token, refresh_token, expires_at):
		self.update_or_create(
			kwargs={"user": user},
			defaults={
				"access_token": access_token,
				"refresh_token": refresh_token,
				"expires_at": expires_at,
			}
		)

class Search_(ModelData):
	def __init__(self, model=SearchInfo):
		super().__init__(model)
	
	def create_or_update(self, data):
		self.update_or_create(
			kwargs={
				"user": data["user"],
				"reccobeats_id": data["reccobeats_id"],
				"spotify_id": data["spotify_id"],
			},
			defaults=data,
		)
	
	def get_searches(self, user):
		searches = self.get_all(filters={"user": user})
		return searches

class Statistics_(ModelData):
	def __init__(self, model=Statistics):
		super().__init__(model)
	
	def create_or_update(self, user, total_songs, tog_genre, rarest_genre, diversity_score, mood_score, all_genres_percent, features_values_average):
		statistic, created = self.update_or_create(
			kwargs={"user": user},
			defaults={ 
				"total_songs": total_songs,
				"most_common_genre_percent": tog_genre,
				"all_genres_percent": all_genres_percent,
				"features_values_average": features_values_average,
				"rarest_genre": rarest_genre,
				"diversity_score": diversity_score,
				"mood_score": mood_score,
			}
		)
		return statistic, created

	def get_statistic(self, user):
		stats = self.get_all(filters={"user": user})
		return stats
	
audio_repo = Audio_()
song_repo = Song_()
features_repo = Features_()
spotify_repo = SpotifyToken_()
search_repo = Search_()
statistics_repo = Statistics_()