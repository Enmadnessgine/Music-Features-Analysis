from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Song, SearchInfo
from .crud import create_song_f
from .forms import AudioUploadForm
from mainapp.utils import info_from_s_to_r, get_features


def analize_audio(request):
    if request.method == "POST":
        upload_file = request.FILES.get('fileToUpload')
        if upload_file:
            song = create_song_f(
                user=request.user,
                file=upload_file,
            )
            messages.success(request, f"Song '{song.title}' uploaded!")
        else:
            messages.error(request, "No file selected!")
    return redirect('profile')

def load_search(request):
    q = request.GET.get('q', "")
    sp_id = None
    rb_id = None
    
    if len(q) == 22:
        sp_id = q
        data = info_from_s_to_r(sp_id)
        rb_id = data['id']
    else:
        sp_id = ""
        rb_id = q
        data = get_features(q)
    
    if "error" in data:
        return render(request, "mainapp/search.html", {"error": data['error'], "q": q})
    
    info = {
        "spotify_id": sp_id,
        "reccobeats_id": rb_id,
        "link": data['href'],
        "acousticness": data['acousticness'],
        "danceability": data['danceability'],
        "energy": data['energy'],
        "instrumentalness": data['instrumentalness'],
        "liveness": data['liveness'],
        "loudness": data['loudness'],
        "speechiness": data['speechiness'],
        "tempo": data['tempo'],
        "valence": data['valence'],
        "user": request.user,
        }
    SearchInfo.objects.create(**info)
        
    return render(request, "mainapp/search.html", {"data": info, "q": q})