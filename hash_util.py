import hashlib

def sha256_str(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()