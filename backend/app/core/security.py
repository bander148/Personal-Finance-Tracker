from authlib.jose import jwt, JoseError
from authlib.jose import JsonWebKey
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from ..config import settings

class JWTManager:
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self._key = JsonWebKey.import_key({'kty': 'oct','k': self.secret_key })

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
        encoded_jwt = jwt.encode(header, to_encode, self._key)
        print(f"🔧 DEBUG: Authlib returned: {type(encoded_jwt)} - {encoded_jwt}")

        # Если это байты - декодируем, если строка - оставляем как есть
        if isinstance(encoded_jwt, bytes):
            print("🔧 DEBUG: Converting bytes to string")
            encoded_jwt = encoded_jwt.decode('utf-8')

        return encoded_jwt
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            if token.startswith("b'") and token.endswith("'"):
                print("🔧 DEBUG: Fixing malformed token string")
                token = token[2:-1]
            decoded = jwt.decode(token,self._key)
            decoded.validate()
            return decoded
        except JoseError:
            return None

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        to_encode.update({
            'exp': expire,
            'iat': datetime.utcnow(),
            'type': 'refresh'
        })
        header = {"alg": self.algorithm}
        encoded_jwt = jwt.encode(header, to_encode, self._key)
        if isinstance(encoded_jwt, bytes):
            encoded_jwt = encoded_jwt.decode('utf-8')

        print(f"🔧 DEBUG: Refresh token type: {type(encoded_jwt)}")
        return encoded_jwt

def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        payload = self.verify_token(refresh_token)
        if not payload or payload.get('type') != 'refresh':
            return None
        access_token_data = {
            "sub": payload.get('sub'),
            "user_id": payload.get('user_id'),
            "email": payload.get('email')
        }
        return self.create_access_token(access_token_data)

jwt_manager = JWTManager()