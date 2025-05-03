from fastapi import FastAPI
from app.models import NoteCreate

app = FastAPI()


#basic route
@app.get("/")
def root():
    return {"message": "Welcome to the AI Notes App!"}


@app.post("/notes")
def create_note(note: NoteCreate):
    return {
        "title": note.title,
        "content": note.content
    }