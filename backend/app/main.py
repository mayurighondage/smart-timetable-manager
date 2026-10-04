from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine, SessionLocal

from .seed import seed_database

from .routers import (
    auth,
    faculty,
    timetable
)


# ==========================================================
# CREATE DATABASE TABLES
# ==========================================================

Base.metadata.create_all(
    bind=engine
)


# ==========================================================
# INSERT DEMO DATA
# ==========================================================

db = SessionLocal()

try:
    seed_database(db)
finally:
    db.close()


# ==========================================================
# CREATE FASTAPI APP
# ==========================================================

app = FastAPI(
    title="EduNova AI Backend",
    description="Smart Timetable & Departmental AI Manager",
    version="1.0.0"
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ==========================================================
# CONNECT ROUTERS
# ==========================================================

app.include_router(
    auth.router
)

app.include_router(
    faculty.router
)

app.include_router(
    timetable.router
)


# ==========================================================
# ROOT API
# ==========================================================

@app.get("/")
def root():

    return {
        "message": "EduNova AI Backend is running",
        "docs": "/docs"
    }


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }