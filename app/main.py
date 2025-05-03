from fastapi import FastAPI
from app.models import NoteCreate
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, Note, get_db


app = FastAPI()


#basic route
@app.get("/")
def root():
    return {"message": "Welcome to the AI Notes App!"}


# @app.post("/notes")
# def create_note(note: NoteCreate):
#     return {
#         "title": note.title,
#         "content": note.content
#     }

@app.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {"id": new_note.id, "title": new_note.title, "content": new_note.content}
