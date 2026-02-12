import pandas as pd
from DataModifying.data.DataBuilder import DataBuilder
import os

def create_features(csv_files: list, raw_folder: str, feature_folder: str):
    r""" Takes ALL raw files with .csv ends, adding column "spotify_id" (if the music have not id - ignore).
        Takes feature csv and add rows + "genre" column.
        final result: feature.csv have data and additional column "genre" with variety of genres,
        SPLITTING THE NAME OF THE .csv BY THE FIRST "_" AND ACCEPTING IT AS A GENRE
    :param csv_files: list of all names, that contains raw_folder
    :param raw_folder: path of the raw csv
    :param feature_folder: path of the feature csv
    """
    for i in csv_files:
        try:
            df = pd.read_csv(os.path.join(raw_folder, i), encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(os.path.join(raw_folder, i), encoding="cp1252")
        name_genre = i.split('_')[0]
        DataBuilder.raw_csv_into_features(df, os.path.join(raw_folder, i),
                                os.path.join(feature_folder, 'features.csv'),
                                name_genre)


if __name__ == '__main__':
    columns = ['acousticness','danceability','energy',
               'instrumentalness','key','liveness','loudness',
               'mode','speechiness','tempo','valence','genre']
    raw_folder = os.path.join(os.getcwd(), 'raw')
    features_folder = os.path.join(os.getcwd(), 'features')

    #       --create new features.csv (Only if you want to overwrite features)--

    # csv_files = [f for f in os.listdir(raw_folder) if f.endswith(".csv")]
    # features = pd.DataFrame(columns=columns)
    # features.to_csv(f'{features_folder}/features.csv', index=False)

