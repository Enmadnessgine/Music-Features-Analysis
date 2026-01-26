from django.shortcuts import redirect
from django.contrib import messages
from ..utils.audio_utils import create_song_f

def analize_audio(request):
	if request.method == "POST":
		upload_file = request.FILES.get('fileToUpload')
		artist = request.POST.get('artist', '')
		title = request.POST.get('title', '')
		
		if upload_file:
			song = create_song_f(
				user=request.user,
				file=upload_file,
	title=title,
				artist=artist,
			)
			messages.success(request, f"Song '{song.title}' uploaded!")
		else:
			messages.error(request, "No file selected!")
	return redirect('profile')