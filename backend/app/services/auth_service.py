from datetime import timedelta
from fastapi import HTTPException, status, Response
from authlib.oauth2 import OAuth2Request
from authlib.oauth2.rfc6749 import grants
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserLogin
from ..core.security import jwt_manager
from ..config import settings
import traceback

class AuthorizationService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, user: UserCreate):
        try:
            print(f"🔧 DEBUG: Starting registration for {user.email}")
            if self.user_repository.get_by_email(user.email):
                print("🔧 DEBUG: User already exists")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )

            print("🔧 DEBUG: Creating user...")
            result = self.user_repository.create_user(user)
            print(f"🔧 DEBUG: User created successfully: {result.id}")
            return result

        except HTTPException:
            print("🔧 DEBUG: HTTPException raised, re-raising")
            raise
        except Exception as e:
            print(f"🔴 ERROR in register_user: {str(e)}")
            print(f"🔴 TRACEBACK: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Registration failed: {str(e)}")

    def login_user(self, user: UserLogin):
        print(f"🔧 DEBUG: Authenticating user {user.email}")
        user_data = self.user_repository.authenticate(user.email, user.password)
        if not user_data:
            print(f"🔧 DEBUG: Authentication failed for {user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        print(f"🔧 DEBUG: Authentication successful for {user.email}")
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
    def verify_token(self, token : str):
        return jwt_manager.verify_token(token)

    def refresh_tokens(self, refresh_token: str):
        try:
            print(f"🔧 DEBUG: Starting token refresh...")
            print(f"🔧 DEBUG: Refresh token: {refresh_token[:50]}...")


            print(f"🔧 DEBUG: Step 1 - Verifying token...")
            payload = self.verify_token(refresh_token)
            print(f"🔧 DEBUG: Token payload: {payload}")

            if not payload:
                print("🔧 DEBUG: ❌ Token verification FAILED")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )


            print(f"🔧 DEBUG: Step 2 - Checking token type...")
            token_type = payload.get('type')
            print(f"🔧 DEBUG: Token type: {token_type}")

            if token_type != 'refresh':
                print(f"🔧 DEBUG: ❌ Wrong token type: {token_type}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type"
                )


            print(f"🔧 DEBUG: Step 3 - Finding user...")
            email = payload.get('email')
            print(f"🔧 DEBUG: Looking for user with email: {email}")

            user = self.user_repository.get_by_email(email)
            if not user:
                print(f"🔧 DEBUG: ❌ User not found: {email}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )

            print(f"🔧 DEBUG: ✅ User found: {user.email} (ID: {user.id})")


            print(f"🔧 DEBUG: Step 4 - Creating new access token...")
            new_access_token = self.create_tokens(user.id, user.email)[0]
            print(f"🔧 DEBUG: ✅ New access token created: {new_access_token[:50]}...")

            return new_access_token

        except HTTPException:
            print("🔧 DEBUG: 🚨 HTTPException raised in refresh_tokens")
            raise
        except Exception as e:
            print(f"🔴 ERROR in refresh_tokens: {e}")
            import traceback
            print(f"🔴 TRACEBACK: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token refresh failed"
            )

    def set_tokens_cookies(self, response: Response, access_token: str, refresh_token: str):
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=False,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite,
            domain=settings.cookie_domain,
            max_age=settings.access_token_expire_minutes * 60,
            path="/",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=False,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite,
            domain=settings.cookie_domain,
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            path = "/",
        )
        print(f"🔧 DEBUG: Cookies set - access_token: {access_token[:20]}...")

    def clear_tokens_cookies(self, response: Response):
        response.delete_cookie("access_token", domain=settings.cookie_domain)
        response.delete_cookie("refresh_token", domain=settings.cookie_domain)

    def set_access_token_cookie(self, response: Response, access_token: str):
        """Установка только access_token cookie"""
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite,
            domain=settings.cookie_domain if settings.cookie_domain else None,
            max_age=settings.access_token_expire_minutes * 60,
            path="/"
        )
        print(f"🔧 DEBUG: New access token cookie set: {access_token[:30]}...")