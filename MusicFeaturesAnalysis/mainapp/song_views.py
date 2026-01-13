from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Song, SearchInfo
from .crud import create_song_f
from .forms import AudioUploadForm
from mainapp.utils import info_from_s_to_r, get_features
from django.http import JsonResponse

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

def load_search(request):
	q = request.GET.get('q', "")
	sp_id = None
	rb_id = None
	
	try:
		if len(q) == 22:
			sp_id = q
			data = info_from_s_to_r(sp_id)
			rb_id = data.get('id', None)
		else:
			sp_id = ""
			rb_id = q
			data = get_features(q)
	except Exception as e:
		return render(request, "mainapp/search.html", {"error": str(e), "q": q})
	
	if not isinstance(data, dict):
		return render(request, "mainapp/search.html", {"error": "Invalid response from API", "q": q})

	if data.get("error"):
		return render(request, "mainapp/search.html", {"error": data["error"], "q": q})
	
	info = {
		"spotify_id": sp_id,
		"reccobeats_id": rb_id,
		"link": data.get('href', ''),
		"acousticness": data.get('acousticness', 0),
		"danceability": data.get('danceability', 0),
		"energy": data.get('energy', 0),
		"instrumentalness": data.get('instrumentalness', 0),
		"liveness": data.get('liveness', 0),
		"loudness": data.get('loudness', 0),
		"speechiness": data.get('speechiness', 0),
		"tempo": data.get('tempo', 0),
		"valence": data.get('valence', 0),
		"user": request.user,
	}
	SearchInfo.objects.create(**info)
		
	return render(request, "mainapp/search.html", {"data": info, "q": q})

def search_ajax(request):
	q = request.GET.get('q', "")
	sp_id = None
	rb_id = None

	try:
		if len(q) == 22:
			sp_id = q
			data = info_from_s_to_r(sp_id)
			rb_id = data['id']
		else:
			sp_id = ""
			rb_id = q
			data = get_features(q)

		if not data:
			return JsonResponse(
				{"ok": False, "error": "id can't be processed", "q": q},
				status=404
			)

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
		}

		SearchInfo.objects.create(user=request.user, **info)

		return JsonResponse({"ok": True, "data": info, "q": q})

	except ConnectionError:
		return JsonResponse(
			{"ok": False, "error": "API unavailable"}, status=503
		)
	except KeyError:
		return JsonResponse(
			{"ok": False, "error": "Track not found"}, status=404
		)