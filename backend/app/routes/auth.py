from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..services.auth_service import AuthorizationService
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserResponse, UserLogin
from ..dependencies.auth import get_current_user
from ..config import settings
router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"]
)

@router.post("/register", response_model=UserResponse)
def register(
        user_data: UserCreate,
        response: Response ,
        db: Session = Depends(get_db),
):
    try:
        user_repository = UserRepository(db)
        auth_service = AuthorizationService(user_repository)
        user = auth_service.register_user(user_data)
        access_token,refresh_token = auth_service.create_tokens(user.id,user.email)
        auth_service.set_tokens_cookies(response,access_token,refresh_token)
        return user
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=UserResponse)
def login(
        user_data: UserLogin,
        response: Response ,
        db: Session = Depends(get_db),
):
    try:
        print(f"🔧 DEBUG: Login attempt for {user_data.email}")

        user_repository = UserRepository(db)
        auth_service = AuthorizationService(user_repository)

        user = auth_service.login_user(user_data)

        access_token, refresh_token = auth_service.create_tokens(user.id, user.email)
        auth_service.set_tokens_cookies(response, access_token, refresh_token)

        print(f"🔧 DEBUG: Login successful for {user.email}")
        return user

    except HTTPException:
        raise
    except Exception as e:
        print(f"🔴 ERROR in login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.get("/logout")
def logout(response: Response):
    auth_service = AuthorizationService(None)
    auth_service.clear_tokens_cookies(response)
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user : User =  Depends(get_current_user)):
    return current_user

@router.post("/validate", response_model=UserResponse)
def validate_token(current_user : User =  Depends(get_current_user)):
    try:
        return current_user
    except Exception as e:
        print(f"🔴 ERROR in validate: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token validation failed"
        )



@router.get("/refresh")
def refresh_token(
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
):
    try:
        print(f"🔧 DEBUG: Refresh endpoint called")
        print(f"🔧 DEBUG: Cookies: {dict(request.cookies)}")

        refresh_token_cookie = request.cookies.get("refresh_token")

        if not refresh_token_cookie:
            print("🔧 DEBUG: No refresh_token in cookies")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found"
            )

        print(f"🔧 DEBUG: Refresh token found: {refresh_token_cookie[:50]}...")

        user_repository = UserRepository(db)
        auth_service = AuthorizationService(user_repository)

        print(f"🔧 DEBUG: Starting token refresh process...")

        print(f"🔧 DEBUG: Step 1 - Verifying token...")
        payload = auth_service.verify_token(refresh_token_cookie)
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

        user = user_repository.get_by_email(email)
        if not user:
            print(f"🔧 DEBUG: ❌ User not found: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        print(f"🔧 DEBUG: ✅ User found: {user.email} (ID: {user.id})")

        print(f"🔧 DEBUG: Step 4 - Creating new access token...")
        access_token, new_refresh_token = auth_service.create_tokens(user.id, user.email)
        print(f"🔧 DEBUG: ✅ New access token created: {access_token[:50]}...")

        print(f"🔧 DEBUG: Step 5 - Setting new cookies...")
        auth_service.set_access_token_cookie(response, access_token)

        auth_service.set_tokens_cookies(response, access_token, new_refresh_token)

        print(f"🔧 DEBUG: ✅ Token refresh completed successfully")

        return {
            "message": "Access token refreshed successfully",
            "user_id": user.id,
            "email": user.email
        }

    except HTTPException:
        print("🔧 DEBUG: HTTPException raised in refresh")
        raise
    except Exception as e:
        print(f"🔴 ERROR in refresh: {str(e)}")
        import traceback
        print(f"🔴 TRACEBACK: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )
@router.get("/debug/cookies")
def debug_cookies(request: Request):
    """Проверка получения cookies на сервере"""
    return {
        "cookies_received": dict(request.cookies),
        "access_token_received": request.cookies.get("access_token"),
        "headers": {
            "user-agent": request.headers.get("user-agent"),
            "origin": request.headers.get("origin"),
        }
    }