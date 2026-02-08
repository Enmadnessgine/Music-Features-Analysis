from pandas.core.interchange.dataframe_protocol import DataFrame


def mapping(df: DataFrame):
    r""" mapping "genre" for every genre.
        Grouping genres from nine to five values:
            Adds additional columns as "genre_mapped" (nine values)
            and "y" (five values)
    :param df: DataFrame that contains features and "genre" column
    """

    df['genre_mapped'] = df['genre'].map(GENRE_TO_GROUP)
    return df['genre_mapped']

GENRE_TO_GROUP = {
    "pop": "vocal",
    "electronic": "energetic",
    "jazz": "acoustic",
    "folk": "acoustic",
    "classical": "calm",
    "ambient": "calm",
    "rock": "energetic",
    "reggae": "vocal",
    "rap": "vocal",
    "hip-hop": "vocal",
}

