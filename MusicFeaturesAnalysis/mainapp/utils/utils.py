from hashlib import sha256

def file_hash(uploaded_file) -> str:
    hasher = sha256()
    for chunk in uploaded_file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()