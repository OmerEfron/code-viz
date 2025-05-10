# /users endpoints (auth, profile)

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from datetime import timedelta, datetime

from backend.database.db import get_db, User, UserTutorialProgress, Session
from backend.models.user import UserCreate, UserProfile, UserProgress, Token, UserProgressUpdate
from backend.auth.auth import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.auth.dependencies import get_current_active_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    # Check if user already exists
    for existing_user in db.memory_db.users.values():
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token
    """
    # Find user by email
    user = None
    for u in db.memory_db.users.values():
        if u.email == form_data.username:
            user = u
            break
            
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=UserProfile)
async def get_user_profile(current_user: User = Depends(get_current_active_user)):
    """
    Get current user's profile
    """
    return current_user

@router.get("/progress", response_model=List[UserProgress])
async def get_user_progress(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's tutorial progress
    """
    progress = []
    for p in db.memory_db.user_tutorial_progress.values():
        if p.user_id == current_user.id:
            progress.append(p)
    
    return progress

@router.post("/progress", response_model=UserProgress)
async def update_user_progress(
    progress_update: UserProgressUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update user's progress on a tutorial
    """
    # Check if progress record exists
    progress = None
    for p in db.memory_db.user_tutorial_progress.values():
        if p.user_id == current_user.id and p.tutorial_id == progress_update.tutorial_id:
            progress = p
            break
    
    if not progress:
        # Create new progress record
        progress = UserTutorialProgress(
            user_id=current_user.id,
            tutorial_id=progress_update.tutorial_id,
            completed=progress_update.completed or False,
            progress_percentage=progress_update.progress_percentage or 0.0,
            last_accessed=datetime.utcnow()
        )
        db.add(progress)
    else:
        # Update existing record
        if progress_update.completed is not None:
            progress.completed = progress_update.completed
        if progress_update.progress_percentage is not None:
            progress.progress_percentage = progress_update.progress_percentage
        progress.last_accessed = datetime.utcnow()
    
    db.commit()
    db.refresh(progress)
    
    return progress
