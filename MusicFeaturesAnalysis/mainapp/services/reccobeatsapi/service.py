import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin

class ReccoAPIError(Exception):
	pass

class ReccoService:
	def __init__(self):
		self.base_url = "https://api.reccobeats.com/v1"

	def _request(
		self,
		method: str,
		endpoint: str,
		params: Optional[Dict[str, Any]] = None,
		json: Optional[Dict[str, Any]] = None,
		files: Optional[Dict[str, Any]] = None,
	) -> Dict[str, Any]:
		url = urljoin(self.base_url + '/',  endpoint)
		
		try:
			response = requests.request(
				method=method,
				url=url,
				params=params,
				json=json,
				files=files,
				headers={"Accept": "application/json"},
			)
			response.raise_for_status()
			return response.json()
		except requests.exceptions.RequestException as e:
			raise ReccoAPIError(f"Recco API error: {e}") from e
		
		
	def get_info_by_id(self, song_id: str):
		endpoint = f"track/{song_id}/audio-features"
		return self._request(
			"GET",
			endpoint=endpoint,
		)
	

	def extract_from_audio(self, file_path: str):
		with open(file_path, "rb") as f:
			files = {"audioFile": ('file', f, 'application/octet-stream')}
			return self._request(
				"POST", 
				"analysis/audio-features",
				files=files
				)
		