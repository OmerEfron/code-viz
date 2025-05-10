# In-memory storage with ORM-like interface

from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Generator
import json

# In-memory storage
class MemoryStorage:
    def __init__(self):
        self.users = {}
        self.tutorials = {}
        self.user_tutorial_progress = {}
        self.next_user_id = 1
        self.next_tutorial_id = 1
        self.next_progress_id = 1

# Global instance
memory_db = MemoryStorage()

# Base model class for all models
class BaseModel:
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

# User model
class User(BaseModel):
    def __init__(self, email: str, username: str, hashed_password: str, 
                 id: Optional[int] = None, created_at: Optional[datetime] = None, 
                 is_active: bool = True):
        self.id = id
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.created_at = created_at or datetime.utcnow()
        self.is_active = is_active

# Tutorial model
class Tutorial(BaseModel):
    def __init__(self, title: str, description: str, difficulty: str, 
                 tags: List[str], content: str, code_examples: List[str],
                 id: Optional[int] = None, created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.id = id
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.tags = tags
        self.content = content
        self.code_examples = code_examples
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at

# UserTutorialProgress model
class UserTutorialProgress(BaseModel):
    def __init__(self, user_id: int, tutorial_id: int, 
                 id: Optional[int] = None, completed: bool = False,
                 last_accessed: Optional[datetime] = None,
                 progress_percentage: float = 0.0):
        self.id = id
        self.user_id = user_id
        self.tutorial_id = tutorial_id
        self.completed = completed
        self.last_accessed = last_accessed or datetime.utcnow()
        self.progress_percentage = progress_percentage

# Session class to mimic SQLAlchemy session
class Session:
    def __init__(self, memory_db):
        self.memory_db = memory_db
        self._query_model = None
        self._filters = []
        
    def query(self, model):
        self._query_model = model
        self._filters = []
        return self
    
    def filter(self, *conditions):
        self._filters.extend(conditions)
        return self
    
    def first(self):
        results = self.all()
        return results[0] if results else None
    
    def all(self):
        if self._query_model == User:
            collection = self.memory_db.users
        elif self._query_model == Tutorial:
            collection = self.memory_db.tutorials
        elif self._query_model == UserTutorialProgress:
            collection = self.memory_db.user_tutorial_progress
        else:
            return []
            
        results = list(collection.values())
        
        # Apply filters
        for condition in self._filters:
            if isinstance(condition, tuple) and len(condition) == 3:
                attr, op, value = condition
                if op == '==':
                    results = [item for item in results if getattr(item, attr) == value]
                elif op == '!=':
                    results = [item for item in results if getattr(item, attr) != value]
                # Add more operators as needed
                
        return results
    
    def add(self, obj):
        if isinstance(obj, User):
            if obj.id is None:
                obj.id = self.memory_db.next_user_id
                self.memory_db.next_user_id += 1
            self.memory_db.users[obj.id] = obj
        elif isinstance(obj, Tutorial):
            if obj.id is None:
                obj.id = self.memory_db.next_tutorial_id
                self.memory_db.next_tutorial_id += 1
            self.memory_db.tutorials[obj.id] = obj
        elif isinstance(obj, UserTutorialProgress):
            if obj.id is None:
                obj.id = self.memory_db.next_progress_id
                self.memory_db.next_progress_id += 1
            self.memory_db.user_tutorial_progress[obj.id] = obj
    
    def commit(self):
        # In a real DB, this would commit the transaction
        pass
    
    def refresh(self, obj):
        # In a real DB, this would refresh the object from the DB
        pass
    
    def close(self):
        # In a real DB, this would close the session
        pass

# Helper function to get DB session
def get_db():
    db = Session(memory_db)
    try:
        yield db
    finally:
        db.close()
