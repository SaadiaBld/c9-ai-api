from pydantic import BaseModel, PositiveFloat, field_validator
from typing import List

class Theme(BaseModel):
    theme: str
    note: PositiveFloat

class VerbatimRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def clean_apostrophes(cls, value):
        return value.replace("'", "’").strip()
    
    @field_validator("text")
    @classmethod
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError("Le texte ne peut pas être vide.")
        return v

class VerbatimResponse(BaseModel):
    themes: List[Theme]
