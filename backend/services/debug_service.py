# Finds bugs and provides context

from backend.utils.parser import CodeParser
from backend.models.code import DebugInput, DebugResult, DebugSuggestion
from typing import List, Dict, Any, Optional
from backend.services.visualize_service import VisualizationService

class DebugService:
    def __init__(self):
        self.visualization_service = VisualizationService()
        
    def debug_code(self, debug_input: DebugInput) -> DebugResult:
        """
        Find bugs in code and provide suggestions
        """
        parser = CodeParser(debug_input.code, debug_input.language)
        
        # Check for syntax errors first
        syntax_error = parser.find_syntax_errors()
        if syntax_error:
            return self._create_syntax_error_result(syntax_error, debug_input)
        
        # Look for logical bugs
        potential_bugs = parser.find_potential_bugs()
        
        # Generate suggestions for each bug
        suggestions = self._generate_suggestions(potential_bugs, debug_input.code)
        
        # Create visualization if needed
        visualization = None
        if len(suggestions) > 0:
            visualization = self.visualization_service.visualize_code(
                CodeInput(code=debug_input.code, language=debug_input.language)
            )
        
        return DebugResult(
            error_type="logical" if potential_bugs else "none",
            error_location=potential_bugs[0].get("line", 0) if potential_bugs else 0,
            error_message=potential_bugs[0].get("message", "") if potential_bugs else "",
            suggestions=suggestions,
            visualization=visualization
        )
    
    def _create_syntax_error_result(self, error: Dict[str, Any], debug_input: DebugInput) -> DebugResult:
        """Create a debug result for syntax errors"""
        suggestion = DebugSuggestion(
            line_number=error["line"],
            original_code="",  # Would extract the relevant line
            suggested_fix="",  # Would generate a fix
            explanation=f"Syntax error: {error['message']}"
        )
        
        return DebugResult(
            error_type="syntax",
            error_location=error["line"],
            error_message=error["message"],
            suggestions=[suggestion],
            visualization=None
        )
    
    def _generate_suggestions(self, bugs: List[Dict[str, Any]], code: str) -> List[DebugSuggestion]:
        """Generate suggestions for each bug"""
        suggestions = []
        
        for bug in bugs:
            # This would be implemented to generate helpful suggestions
            suggestion = DebugSuggestion(
                line_number=bug.get("line", 0),
                original_code="",  # Would extract the relevant line
                suggested_fix="",  # Would generate a fix
                explanation=bug.get("message", "")
            )
            suggestions.append(suggestion)
            
        return suggestions
