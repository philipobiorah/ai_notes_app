from fastapi import FastAPI
from app.models import NoteCreate
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, Note, get_db
from app.sentiment_analyzer import analyze_sentiment
from app.auth import verify_api_key

app = FastAPI()



#basic route
@app.get("/")
def root(_: str = Depends(verify_api_key)):
    return {"message": "Welcome to the AI Notes App!"}


# @app.post("/notes")
# def create_note(note: NoteCreate):
#     return {
#         "title": note.title,
#         "content": note.content
#     }


# Create a new note
@app.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db), _: str = Depends(verify_api_key)):
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {"id": new_note.id, "title": new_note.title, "content": new_note.content}

# Get all notes
@app.get("/notes")
def get_notes(db: Session = Depends(get_db), _: str = Depends(verify_api_key)):
    notes = db.query(Note).all()
    return [{"id": note.id, "title": note.title, "content": note.content} for note in notes]
            

#/notes/{note_id}/analyze
@app.get("/notes/{note_id}/analyze")
def analyze_note_sentiment(note_id: int, db: Session = Depends(get_db), _: str = Depends(verify_api_key)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        return {"error": "Note not found"}
    sentiment = analyze_sentiment(note.content)
    return {
        "id": note.id,
        "title": note.title,
        "sentiment": sentiment
    }
