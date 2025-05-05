from pydantic import BaseModel, Field

class NoteCreate(BaseModel):
    
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=10)