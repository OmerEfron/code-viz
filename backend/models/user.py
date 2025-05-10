# Pydantic models for user

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        orm_mode = True

class UserProgress(BaseModel):
    user_id: int
    tutorial_id: int
    completed: bool
    last_accessed: datetime
    progress_percentage: float
    
    class Config:
        orm_mode = True

class UserProgressUpdate(BaseModel):
    tutorial_id: int
    completed: Optional[bool] = None
    progress_percentage: Optional[float] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
