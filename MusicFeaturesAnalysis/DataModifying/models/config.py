
FEATURE_COLS = [
    "acousticness",
    "danceability",
    "energy",
    "instrumentalness",
    "liveness",
    "loudness",
    "speechiness",
    "tempo",
    "valence",
]

GROUPS = {
    'vocal' : ["pop", "reggae", "rap", 'hip-hop'],
    'energetic' : ["electronic", "rock"],
    'calm' : ["ambient", "classical"],
    'acoustic' : ["jazz", "folk"],
}

VECTOR_FIELDS = ['energy', 'acousticness', 'tempo', 'danceability', 'instrumentalness', 'loudness',
                  'liveness', 'speechiness', 'valence', 'calm', 'vocal', 'acoustic', 'energetic', "pop",
                  "reggae", "rap", 'hip-hop', "electronic", "rock", "ambient", "classical", "jazz",
                  "folk", "mood"]



