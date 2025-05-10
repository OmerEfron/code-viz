from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class CodeInput(BaseModel):
    code: str
    language: str = "python"

class VisualizationStep(BaseModel):
    step_number: int
    line_number: int
    description: str
    variables: Dict[str, Any]
    memory_state: Optional[Dict[str, Any]]

class CodeVisualization(BaseModel):
    steps: List[VisualizationStep]
    total_steps: int

class DebugInput(BaseModel):
    code: str
    language: str = "python"
    error_message: Optional[str] = None

class DebugSuggestion(BaseModel):
    line_number: int
    original_code: str
    suggested_fix: str
    explanation: str

class DebugResult(BaseModel):
    error_type: str
    error_location: int
    error_message: str
    suggestions: List[DebugSuggestion]
    visualization: Optional[CodeVisualization]
