from authlib.jose import jwt, JoseError
from authlib.jose import JsonWebKey
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from ..config import settings

class JWTManager:
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self._key = JsonWebKey.generate_key('oct', 256, is_private=True)

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else :
            expire = datetime.utcnow() + timedelta(minutes = settings.access_token_expire_minutes)
        to_encode.update({
            'exp': expire,
            'iat': datetime.utcnow(),
            'type': 'access'
        })
        header = {"alg": self.algorithm}
        return jwt.encode(to_encode, self._key, headers=header)

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            decoded = jwt.decode(token,self._key)
            decoded.validate()
            return decoded
        except jwt.InvalidTokenError:
            return None

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes = settings.refresh_token_expire_minutes)
        to_encode.update({
            'exp': expire,
            'iat': datetime.utcnow(),
            'type': 'refresh'
        })
        header = {"alg": self.algorithm}
        return jwt.encode(to_encode, self._key, headers=header)

    def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        payload = jwt.verify_token(refresh_token)
        if not payload or payload.get('type') != 'refresh':
            return None
        access_token_data = {
            "sub": payload.get('sub'),
            "user_id": payload.get('user_id'),
            "email": payload.get('email')
        }
        return self.create_access_token(access_token_data)

jwt_manager = JWTManager()