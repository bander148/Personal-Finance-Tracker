from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..services.auth_service import AuthorizationService
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserResponse, UserLogin
from ..dependencies.auth import get_current_user

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
    user_repository = UserRepository(db)
    auth_service = AuthorizationService(user_repository)
    user = user_repository.create_user(user_data)
    access_token,refresh_token = auth_service.create_tokens(user.id,user.email)
    auth_service.set_tokens_cookies(response,access_token,refresh_token)
    return user

@router.get("/login", response_model=UserResponse)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
        response: Response = None
):
    user_repository = UserRepository(db)
    auth_service = AuthorizationService(user_repository)
    user = auth_service.login_user(UserLogin)
    access_token,refresh_token = auth_service.create_tokens(user.id,user.email)
    auth_service.set_tokens_cookies(response,access_token,refresh_token)
    return user

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