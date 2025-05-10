# /code endpoints (visualize, debug)

from fastapi import APIRouter, Depends, HTTPException

from backend.database.db import get_db, Session
from backend.models.code import CodeInput, CodeVisualization, DebugInput, DebugResult
from backend.services.visualize_service import VisualizationService
from backend.services.debug_service import DebugService

router = APIRouter(
    prefix="/code",
    tags=["code"]
)

@router.post("/visualize", response_model=CodeVisualization)
async def visualize_code(
    code_input: CodeInput,
    db: Session = Depends(get_db)
):
    """
    Visualize code execution steps
    """
    visualization_service = VisualizationService()
    result = visualization_service.visualize_code(code_input)
    return result

@router.post("/debug", response_model=DebugResult)
async def debug_code(
    debug_input: DebugInput,
    db: Session = Depends(get_db)
):
    """
    Debug code and provide suggestions
    """
    debug_service = DebugService()
    result = debug_service.debug_code(debug_input)
    return result

@router.post("/parse", response_model=bool)
async def parse_code(
    code_input: CodeInput,
    db: Session = Depends(get_db)
):
    """
    Parse code and return True if valid, False otherwise
    """
    parser = CodeParser(code_input.code, code_input.language)
    return parser.extract_variables()