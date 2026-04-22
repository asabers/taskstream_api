import hmac
import hashlib
import os
from datetime import datetime, timedelta
from jose import jwt

# Hardcoded secret
SECRET_KEY = "SUPER_SECRET_KEY_123" 
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    """
    TRAP: An agent should flag this. 
    It uses manual HMAC-SHA256 comparison instead of passlib/bcrypt.
    """
    key = SECRET_KEY.encode()
    msg = plain_password.encode()
    digest = hmac.new(key, msg, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, hashed_password)

def get_password_hash(password):
    key = SECRET_KEY.encode()
    msg = password.encode()
    return hmac.new(key, msg, hashlib.sha256).hexdigest()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def validate_token_integrity(token: str):
    # Contextual Ambiguity: This is defined but never called in main.py
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload if payload.get("sub") else None
    except Exception:
        return None