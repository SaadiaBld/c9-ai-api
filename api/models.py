from pydantic import BaseModel, PositiveFloat, validator
from typing import List

class Theme(BaseModel):
    theme: str
    note: PositiveFloat

class VerbatimRequest(BaseModel):
    text: str

    @validator("text")
    def clean_apostrophes(cls, value):
        return value.replace("'", "’").strip()

class VerbatimResponse(BaseModel):
    themes: List[Theme]
