from functools import wraps

def des(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as e:
			print(f"API call failed: {e}")
			return {"error": "id is not valid"}

	return wrapper