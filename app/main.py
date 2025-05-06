from fastapi import FastAPI, HTTPException
from app.models import NoteCreate
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, Note, get_db
from app.sentiment_analyzer import analyze_sentiment
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from app.auth_jwt import authenticate_user, create_access_token, verify_jwt_token


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#basic route
@app.get("/")
def root(username: str = Depends(verify_jwt_token)):
    return {"message": "Welcome to the AI Notes App!"}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


# Create a new note
@app.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db), username: str = Depends(verify_jwt_token)):
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {"id": new_note.id, "title": new_note.title, "content": new_note.content}

# Get all notes
@app.get("/notes")
def get_notes(db: Session = Depends(get_db), username: str = Depends(verify_jwt_token)):
    notes = db.query(Note).all()
    return [{"id": note.id, "title": note.title, "content": note.content} for note in notes]
            

#/notes/{note_id}/analyze
@app.get("/notes/{note_id}/analyze")
def analyze_note_sentiment(note_id: int, db: Session = Depends(get_db), username: str = Depends(verify_jwt_token)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        return {"error": "Note not found"}
    sentiment = analyze_sentiment(note.content)
    return {
        "id": note.id,
        "title": note.title,
        "sentiment": sentiment
    }
