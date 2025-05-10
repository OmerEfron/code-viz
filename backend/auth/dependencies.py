# Auth dependencies for routes

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.database.db import get_db, User, Session
from backend.auth.auth import verify_token
from backend.models.user import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token, credentials_exception)
    
    # Find user by email
    user = None
    for u in db.memory_db.users.values():
        if u.email == token_data.email:
            user = u
            break
            
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
