from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TutorialBase(BaseModel):
    title: str
    description: str
    difficulty: str
    tags: List[str]

class TutorialCreate(TutorialBase):
    content: str
    code_examples: List[str]

class Tutorial(TutorialBase):
    id: int
    content: str
    code_examples: List[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

class TutorialList(BaseModel):
    tutorials: List[Tutorial]
