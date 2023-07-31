from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

# to run type:
# uvicorn books:app --reload

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Book(BaseModel):
    # id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(ge=1, le=101)

BOOKS = []

@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@app.post("/")
def create_book(book: Book, db: Session = Depends(get_db)):
    # BOOKS.append(book)
    
    book_model = models.Book()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book

@app.put("/{book_id}")
def update_book(book_id: int, book: Book, db: Session = Depends(get_db)):
    # counter = 0

    # for x in BOOKS:
    #     counter += 1
    #     if x.id == book_id:
    #         BOOKS[counter-1] = book
    #         return BOOKS[counter-1]

    book_model = db.query(models.Book).filter(models.Book.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404, 
            detail=f"ID {book_id} not found"
        )
    
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book

@app.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    # counter = 0

    # for x in BOOKS:
    #     counter += 1
    #     if x.id == book_id:
    #         del BOOKS[counter-1]
    #         return {"message": "Deleted book"}

    book_model = db.query(models.Book).filter(models.Book.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} not found"
        )
    
    db.query(models.Book).filter(models.Book.id == book_id).delete()

    db.commit()

