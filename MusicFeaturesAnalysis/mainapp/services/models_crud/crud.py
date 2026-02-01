from ..model_db import ModelData
from mainapp.models import Song, SearchInfo, SpotifyToken, AudioFile, Features

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


audio_repo = Audio_()
song_repo = Song_()
features_repo = Features_()