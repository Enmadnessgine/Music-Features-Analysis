import os
import django
import numpy as np
import joblib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MusicFeaturesAnalysis.settings')
django.setup()

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from mainapp.models import Statistics

def retrain_kmeans(n_clusters=5):

    data = Statistics.objects.values_list('id', 'user_vector')

    ids = []
    vectors = []

    for item in data:
        if item[1] is not None:
            ids.append(item[0])
            vectors.append(item[1])

    X = np.array(vectors)


    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)


    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(X_scaled)


    for obj_id, label in zip(ids, labels):
        Statistics.objects.filter(id=obj_id).update(cluster_id=int(label))


    joblib.dump(scaler, "DataModifying/models/artifacts/scaler.pkl")
    joblib.dump(kmeans, "DataModifying/models/artifacts/kmeans.pkl")

    print("KMeans retrained successfully.")


if __name__ == "__main__":
    retrain_kmeans()