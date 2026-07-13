# T008 — Pydantic schemas (ตรงกับ contracts/openapi.yaml)
from typing import Optional, Literal
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)   # FR-001, FR-009
    description: Optional[str] = None


class TaskUpdate(BaseModel):                            # FR-005
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: Literal["pending", "done"]
    created_at: str
    completed_at: Optional[str]
