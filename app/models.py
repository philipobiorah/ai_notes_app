from pydantic import BaseModel, Field

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, example="My Note Title")
    content: str = Field(..., min_length=1, example="This is the content of my note.")