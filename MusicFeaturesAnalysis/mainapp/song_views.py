from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Song
from .crud import create_song_f
from .forms import AudioUploadForm


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