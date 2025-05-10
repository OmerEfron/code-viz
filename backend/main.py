# FastAPI app entry point

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import users, tutorials, code, llm

app = FastAPI(
    title="Code Learning Platform API",
    description="API for a platform to learn coding through visualization and debugging",
    version="0.1.0"
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(tutorials.router)
app.include_router(code.router)
app.include_router(llm.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Code Learning Platform API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
