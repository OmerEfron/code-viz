# LLM-specific routes (optional)

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from backend.database.db import get_db, Session
from backend.models.code import CodeInput
from backend.services.llm_service import LLMService

router = APIRouter(
    prefix="/llm",
    tags=["llm"]
)

@router.post("/explain", response_model=Dict[str, Any])
async def explain_code(
    code_input: CodeInput,
    db: Session = Depends(get_db)
):
    """
    Get an explanation of code using LLM
    """
    llm_service = LLMService()
    explanation = await llm_service.generate_code_explanation(
        code_input.code, 
        code_input.language
    )
    
    return {"explanation": explanation}

@router.post("/improve", response_model=Dict[str, Any])
async def improve_code(
    code_input: CodeInput,
    db: Session = Depends(get_db)
):
    """
    Get suggestions to improve code using LLM
    """
    llm_service = LLMService()
    improvements = await llm_service.suggest_code_improvements(
        code_input.code, 
        code_input.language
    )
    
    return improvements

@router.post("/debug", response_model=Dict[str, Any])
async def llm_debug(
    debug_input: CodeInput,
    error_message: str = None,
    db: Session = Depends(get_db)
):
    """
    Debug code using LLM
    """
    llm_service = LLMService()
    debug_result = await llm_service.debug_with_llm(
        debug_input.code,
        error_message
    )
    
    return debug_result
