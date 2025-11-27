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
    return { "valid": True,"user" : current_user.email }

@router.get("/refresh", response_model=UserResponse)
def refresh_token(
        request : Request,
        response: Response,
        db: Session = Depends(get_db),
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )
    user_repository = UserRepository(db)
    auth_service = AuthorizationService(user_repository)
    new_access_token = auth_service.refresh_tokens(refresh_token)
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain,
        max_age=settings.access_token_expire_minutes * 60
    )
    return {"message": "Access token refreshed"}
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