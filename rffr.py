import requests
file_path = "song.mp3"
url = "https://www.freeconvert.com/mp3-compressor/download"

with open(file_path, "rb") as f:
    files = {"files": f}
    response = requests.request("POST", url, files=files)
    
response.raise_for_status()

if response.status_code == 200:
    with open("song_compressed.mp3", "wb") as out:
        out.write(response.content)
else:
    print("Error:", response.status_code)