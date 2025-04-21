# Data models for the Soul Profile# soul_engine/model.py
from pydantic import BaseModel, Field
from typing import List, Optional

class SoulProfile(BaseModel):
    background_context: Optional[str] = None
    core_values: List[str] = Field(default_factory=list)
    motivations: List[str] = Field(default_factory=list)
    fears: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    worldview: Optional[str] = None
    user_notes: Optional[str] = None
