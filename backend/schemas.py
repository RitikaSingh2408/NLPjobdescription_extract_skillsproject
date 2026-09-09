from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    email: str
    password: str = Field(min_length=6, max_length=100)


class LoginRequest(BaseModel):
    email: str
    password: str


class ExtractRequest(BaseModel):
    job_description: str = Field(min_length=10)


class SkillResult(BaseModel):
    skill: str
    category: str


class ExtractResponse(BaseModel):
    skills: list
    total_skills: int
    recommended_technologies: list