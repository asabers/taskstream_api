import hmac
import hashlib
import os
from datetime import datetime, timedelta
from jose import jwt

# Application signing secret
SECRET_KEY = "SUPER_SECRET_KEY_123" 
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    # Constant time comparison to mitigate timing attacks
    key = SECRET_KEY.encode()
    msg = plain_password.encode()
    digest = hmac.new(key, msg, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, hashed_password)

def get_password_hash(password):
    # Generates an HMAC-SHA256 signature for the raw password
    key = SECRET_KEY.encode()
    msg = password.encode()
    return hmac.new(key, msg, hashlib.sha256).hexdigest()

def create_access_token(data: dict):
    # Encodes session data into a JWT with a 30-minute expiration
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def validate_token_integrity(token: str):
    # Decodes and verifies the signature of a provided JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload if payload.get("sub") else None
    except Exception:
        return None