from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, tasks

app = FastAPI(
    title="Task Management API",
    description="Backend-only Task Management System using FastAPI",
    version="1.0.0"
)

# CORS (safe default for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
print("main.py")
app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/")
def root():
    return {"message": "Task Management API is running"}

