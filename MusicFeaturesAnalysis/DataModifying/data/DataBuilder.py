import requests
import pandas as pd
from time import sleep
from dotenv import load_dotenv
import os

from pandas.core.interchange.dataframe_protocol import DataFrame
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

sp = Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                   client_secret=client_secret))

class DataBuilder:
    @staticmethod
    def get_features(id: str) -> dict | Exception:
        r""" basic feature extraction from ReccoBeats.
        :param id: ReccoBeats ID
        :return: dictionary object
        :rtype: dict
        :raise ValueError: Incorrect id
        """
        res = requests.get(f"https://api.reccobeats.com/v1/track/{id}/audio-features")
        if res.status_code == 200:
            json_object = res.json()
            return json_object
        else:
            raise ValueError(f"Помилка API! Статус: {res.status_code}; Текст відповіді: {res.text}")

    @staticmethod
    def get_info(id: str) -> dict | None | Exception:
        r""" all covered info about ID song.
        To get the ReccoBeats ID use return_result['content'][0]['id']
        :param id: Spotify ID
        :return: dictionary object
        :rtype: dict
        :raise ValueError: Incorrect id
        :raises e: Loss problem
        """
        params = {"ids": f"GET /track?ids={id}"}
        r = requests.get(f'https://api.reccobeats.com/v1/track?ids={id}')
        try:
            data = r.json()
            if data['content']:
                return data
            else:
                return None
        except Exception as e:
            raise e

    @staticmethod
    def get_spotify_id(song_name: str, artist_name: str) -> str | None:
        r""" Spotify ID by artist name and song name by using Spotify API.
        :param song_name: Name of the song (raw data)
        :param artist_name: Name of the artist (raw data)
        :return: Spotify ID of the track, if not found - None
        :rtype: str
        """
        query = f"track:{song_name} artist:{artist_name}"
        result = sp.search(q=query, type="track", limit=1)
        items = result['tracks']['items']
        if items:
            return items[0]['id']
        return None

    @staticmethod
    def add_csv_id(df: DataFrame, csv_path: str):
        r""" improve raw data by adding spotify ID as third column.
            If inside the file there was some id, it will ignore them
        :param df: DataFrame of the raw data
        :param csv_path: Path where csv belongs
        :raise e: One of the trouble: Spotify ID/API
        """
        for i in range(len(df)):
            if pd.notna(df.loc[i, "spotify_id"]) and df.loc[i, "spotify_id"] != "":
                continue

            song = df.loc[i, "song_name"]
            artist = df.loc[i, "artist_name"]

            try:
                spotify_id = DataBuilder.get_spotify_id(song, artist)
                df.loc[i, "spotify_id"] = spotify_id

                # print(f"{i + 1}/{len(df)}: {song} - {artist} => {spotify_id}")
                sleep(0.2)
            except Exception as e:
                print(f"Помилка для {song} - {artist}: {e}")
                raise e

            df.to_csv(csv_path, index=False)

    @staticmethod
    def create_features_csv(df: DataFrame, csv_path: str, genre: str):
        r""" adds features into csv that contains at least "spotify_id" column.
            creates additional column "genre" due to supervised learning models.
            If ReccoBeats didnt match any - ignore row.
        :param df: DataFrame of the raw data with "spotify_id" column
        :param csv_path: path of the feature csv
        :param genre: music genre that will be transfer
        """
        for i in range(len(df)):
            spotify_id = df['spotify_id'][i]
            reccobeats_id = DataBuilder.get_info(spotify_id)
            if reccobeats_id == None:
                continue
            features = DataBuilder.get_features(reccobeats_id['content'][0]['id'])
            df2 = pd.DataFrame([features]).drop(['id', 'isrc', 'href'], axis=1)
            df2.loc[0, 'genre'] = genre
            df2.to_csv(csv_path,  mode='a', index=False, header=False)

    @staticmethod
    def raw_csv_into_features(df: DataFrame, csv_raw: str, csv_feature: str, genre: str):
        r""" Takes the raw data, adding column "spotify_id" (if the music have not id - ignore).
            Takes feature csv and add rows + "genre" column.
            final result: feature.csv have data and additional column "genre"
        :param df: DataFrame of the raw data
        :param csv_raw: path of the raw csv
        :param csv_feature: path of the feature csv
        :param genre: music genre that will be transfer
        """
        DataBuilder.add_csv_id(df, csv_raw)
        DataBuilder.create_features_csv(df, csv_feature, genre)