from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://35.78.101.190",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from inside a Docker container!"}

# --- Models ---
class Note(BaseModel):
    id: Optional[int] = None # ID giờ là không bắt buộc khi tạo
    title: str
    content: str

# Model cho việc cập nhật, không cần ID
class NoteUpdate(BaseModel):
    title: str
    content: str

# --- "Fake" Database ---
db: List[Note] = []
note_counter = 0

# --- API Endpoints ---

@app.post("/notes/", response_model=Note)
def create_note(note: Note):
    global note_counter
    note.id = note_counter
    db.append(note)
    note_counter += 1
    return note

@app.get("/notes/", response_model=List[Note])
def get_notes():
    return db

@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int):
    for note in db:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")

@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, note_update: NoteUpdate):
    for note in db:
        if note.id == note_id:
            note.title = note_update.title
            note.content = note_update.content
            return note
    raise HTTPException(status_code=404, detail="Note not found")

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for index, note in enumerate(db):
        if note.id == note_id:
            db.pop(index)
            return {"message": "Note deleted successfully"}
    raise HTTPException(status_code=404, detail="Note not found")
