from django.shortcuts import render
from django.http import JsonResponse
from ..models import SearchInfo
from ..utils.info_utils import info_from_s_to_r, get_features
from ..utils.search_utils import resolve_song, build_info

def load_search(request):
	q = request.GET.get('q', "")
	try:
		sp_id, rb_id, data = resolve_song(q)
		info = build_info(sp_id, rb_id, data, request.user)
		if not isinstance(data, dict):
			return render(request, "mainapp/search.html", {"error": "Invalid response from API", "q": q})
		if data.get("error"):
			return render(request, "mainapp/search.html", {"error": data["error"], "q": q})
		SearchInfo.objects.create(**info)
	except Exception as e:
		return render(request, "mainapp/search.html", {"error": str(e), "q": q})

	return render(request, "mainapp/search.html", {"data": info, "q": q})

def search_ajax(request):
	q = request.GET.get("q", "")
	try:
		sp_id, rb_id, data = resolve_song(q)
		if not isinstance(data, dict):
			return JsonResponse(
				{"ok": False, "error": "Invalid response from API", "q": q},
				status=500
			)
		if data.get("error"):
			return JsonResponse(
				{"ok": False, "error": data["error"], "q": q},
				status=404
			)
		info = build_info(sp_id, rb_id, data, request.user)
		SearchInfo.objects.create(**info)
		return JsonResponse({"ok": True, "data": info, "q": q})

	except ConnectionError:
		return JsonResponse(
			{"ok": False, "error": "API unavailable"},
			status=503
		)

	except Exception as e:
		return JsonResponse(
			{"ok": False, "error": str(e)},
			status=500
		)