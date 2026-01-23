import requests
from cryptography.fernet import Fernet

def get_features(id):
        res = requests.get(f"https://api.reccobeats.com/v1/track/{id}/audio-features")
        if res.status_code == 200:
            json_object = res.json()
            return json_object
        else:
            raise ConnectionError("Maybe try later")


def get_info(id):
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
            return data
    except Exception as e:
        raise e


print(Fernet.generate_key().decode())

#reccobeats_id = get_info("0pqnGHJpmpxLKifKRmU6WP")['content'][0]['id']

#print(get_features(reccobeats_id))
