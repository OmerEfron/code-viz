# Project Summary

> **Note**: This document serves as the primary reference for all cursor rules and project guidelines. All team members should refer to this document for context and direction regarding the project's components, user flows, and integration strategies.

## System Components Overview
### Frontend
- Built using React.
- Provides a user interface for inputting code snippets, viewing tutorials, and interacting with visualizations.

### Backend
- Built using Python with FastAPI.
- Handles API requests for code processing and visualization generation.

### Visualization Engine
- Uses HTML5 Canvas API or WebGL for rendering 2D graphics.

### LLM Integration
- Powers features such as code-to-visualization translation and debugging insights.

### User Management
- Handles user accounts and progress tracking.

## Primary Personas
- **Students and Beginners**: Learn coding concepts through interactive visualizations.
- **Educators**: Create and share lessons with visual aids.
- **Hobbyists and Developers**: Test and explore code snippets.

## Key User Flows
- **Learning Flow**: User selects a tutorial and views animations.
- **Debugging Flow**: User submits buggy code for analysis.
- **Code Visualization Flow**: User writes or uploads code snippets.

## System Architecture Overview
- Composed of a React frontend, FastAPI backend, visualization engine, and LLM integration.

## Features Overview
- Code Execution Visualization
- Interactive Debugging
- Tutorials and Learning Paths
- Natural Language Processing

## Integration Strategy
- Frontend communicates with the backend via REST API.
- LLM accessed via secure HTTP API.