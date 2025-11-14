"""
schemas.py — Shared data schemas (placeholder)

This file should contain Pydantic models matching the TypeScript interfaces
in shared/schema.ts to ensure type safety across frontend and backend.

Backend Implementation Steps:
1. Install Pydantic: pip install pydantic
2. Define models matching frontend TypeScript interfaces
3. Add validation rules (min/max values, required fields)
4. Export for use in FastAPI endpoints

Example Schema Definitions:

from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

class RunConfig(BaseModel):
    lr: float = Field(gt=0, description="Learning rate")
    epochs: int = Field(gt=0, description="Number of epochs")
    batch_size: int = Field(gt=0, description="Batch size")

class Run(BaseModel):
    id: str
    status: Literal["pending", "running", "completed", "failed"]
    config: RunConfig
    val_loss: Optional[float] = None
    lr_used: Optional[float] = None
    created_at: Optional[datetime] = None

class ChatMessage(BaseModel):
    id: str
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime
    runConfigs: Optional[list[RunConfig]] = None

This file is intentionally left incomplete for backend teammates to implement.
"""

# TODO: Install Pydantic
# TODO: Define RunConfig, Run, ChatMessage models
# TODO: Add validation rules
# TODO: Ensure models match TypeScript interfaces exactly
