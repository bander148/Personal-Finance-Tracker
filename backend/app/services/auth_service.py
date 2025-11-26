from datetime import timedelta
from fastapi import HTTPException, status, Response
from authlib.oauth2 import OAuth2Request
from authlib.oauth2.rfc6749 import grants
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserLogin
from ..core.security import jwt_manager
from ..config import settings

class AuthorizationService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, user: UserCreate):
        if self.user_repository.get_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        return self.user_repository.create_user(user)

    def login_user(self, user: UserLogin):
        user_data =  self.user_repository.authenticate(user.email, user.password)
        if not user_data:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password")
        return user_data

    def create_tokens(self, user_id: int, email: str):
        token_data = {
            "sub": email,
            "user_id": user_id,
            "email": email
        }

        access_token = jwt_manager.create_access_token(token_data)
        refresh_token = jwt_manager.create_refresh_token(token_data)

        return access_token, refresh_token
    def varify_token(self, token : str):
        return jwt_manager.varify_token(token)

    def refresh_tokens(self, refresh_token : str):
        new_access_token = jwt_manager.refresh_access_token(refresh_token)
        if not new_access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        return new_access_token

    def set_tokens_cookies(self, response: Response, access_token: str, refresh_token: str):
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite,
            domain=settings.cookie_domain,
            max_age=settings.access_token_expire_minutes * 60
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite,
            domain=settings.cookie_domain,
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60
        )

    def clear_tokens_cookies(self, response: Response):
        response.delete_cookie("access_token", domain=settings.cookie_domain)
        response.delete_cookie("refresh_token", domain=settings.cookie_domain)