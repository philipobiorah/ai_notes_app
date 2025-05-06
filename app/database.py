from sqlalchemy import create_engine, Column, Integer, String, Text 
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

import os

os.makedirs("./data", exist_ok=True)


#SQLite database URL
# DATABASE_URL = "sqlite:///./notes.db"
# # to persitent data 
DATABASE_URL = "sqlite:///./data/notes.db"


# Create a new SQLite database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a base class for declarative models
Base = declarative_base()

# Create a session factory
SessionLocal = sessionmaker(bind=engine)    

#create a mode the notes l fortable
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text, nullable=False)

# Create the database tables
Base.metadata.create_all(bind=engine)


# Create a new session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    