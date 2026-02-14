from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List
from uuid import uuid4

# FastAPI instance (must be named 'app' as per assignment)
app = FastAPI(title="Mini Resume Collector API")

# In-memory storage (no database required)
resumes = []


# =========================
# Pydantic Models
# =========================

class Resume(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    skills: List[str]
    experience_years: float = Field(..., ge=0)


class ResumeResponse(Resume):
    id: str


# =========================
# Endpoints
# =========================

# Root Endpoint (optional but useful)
@app.get("/")
def root():
    return {"message": "Mini Resume Collector API is running"}


# Health Check Endpoint (Required)
@app.get("/health", status_code=200)
def health_check():
    return {"status": "healthy"}


# Create Resume
@app.post("/resumes", status_code=201, response_model=ResumeResponse)
def create_resume(resume: Resume):
    resume_id = str(uuid4())

    # Pydantic v2 uses model_dump() instead of dict()
    resume_data = resume.model_dump()

    resume_data["id"] = resume_id
    resumes.append(resume_data)

    return resume_data


# Get All Resumes
@app.get("/resumes", response_model=List[ResumeResponse])
def get_resumes():
    return resumes


# Get Resume by ID
@app.get("/resumes/{resume_id}", response_model=ResumeResponse)
def get_resume(resume_id: str):
    for resume in resumes:
        if resume["id"] == resume_id:
            return resume

    raise HTTPException(status_code=404, detail="Resume not found")
