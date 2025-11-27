from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.auth_service import AuthorizationService
from ..repositories.user_repository import UserRepository

security = HTTPBearer(auto_error=False)

async def get_current_user(
        request : Request,
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user_repository = UserRepository(db)
    auth_service = AuthorizationService(user_repository)

    token = None
    if credentials and credentials.credentials:
        token = credentials.credentials

    if not token and request:
        token = request.cookies.get("access_token")

    if not token and request:
        token = request.query_params.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = auth_service.verify_token(token)
    if not payload or payload["type"] != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email = payload.get("sub")
    user = user_repository.get_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
async def get_current_user_optional(
        request: Request = None,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    try:
        return await get_current_user(request, credentials, db)
    except HTTPException:
        return None