from pandas.core.interchange.dataframe_protocol import DataFrame


def mapping(df: DataFrame, features_folder_path: str):
    r""" mapping "genre" for every genre.
        Grouping genres from nine to five values:
            Adds additional columns as "genre_mapped" (nine values)
            and "y" (five values)
    :param df: DataFrame that contains features and "genre" column
    :param features_folder_path: feature path
    """
    df['genre_mapped'] = df['genre'].map(GENRE_TO_GROUP)
    df['y'] = df['genre_mapped'].map(GROUP_TO_ID)
    df.to_csv(f'{features_folder_path}/features.csv', index=False)


GENRE_TO_GROUP = {
    "pop": "urban",
    "electronic": "urban",
    "hip-hop": "urban",
    "jazz": "acoustic",
    "folk": "acoustic",
    "classical": "calm",
    "ambient": "calm",
    "rock": "rock",
    "reggae": "reggae"
}
GROUP_TO_ID = {
    "urban": 0,
    "acoustic": 1,
    "calm": 2,
    "rock": 3,
    "reggae": 4
}

ID_TO_GROUP = {v: k for k, v in GROUP_TO_ID.items()}
