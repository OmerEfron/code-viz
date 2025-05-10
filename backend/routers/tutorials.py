# /tutorials endpoints

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from backend.database.db import get_db, Tutorial as DBTutorial, User, Session
from backend.models.tutorial import Tutorial, TutorialList
from backend.auth.dependencies import get_current_active_user

router = APIRouter(
    prefix="/tutorials",
    tags=["tutorials"]
)

@router.get("", response_model=List[Tutorial])
async def get_tutorials(
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get a list of all tutorials
    """
    tutorials = list(db.memory_db.tutorials.values())
    # Apply skip and limit
    return tutorials[skip:skip+limit]

@router.get("/{tutorial_id}", response_model=Tutorial)
async def get_tutorial(
    tutorial_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific tutorial by ID
    """
    tutorial = db.memory_db.tutorials.get(tutorial_id)
    if not tutorial:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return tutorial

@router.post("/progress")
async def update_tutorial_progress(
    tutorial_id: int,
    progress_percentage: float,
    completed: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update user's progress on a tutorial
    """
    # This is handled in the users router, but we provide this endpoint for convenience
    from backend.routers.users import update_user_progress
    from backend.models.user import UserProgressUpdate
    
    progress_update = UserProgressUpdate(
        tutorial_id=tutorial_id,
        completed=completed,
        progress_percentage=progress_percentage
    )
    
    return await update_user_progress(progress_update, current_user, db)
