from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from .schemas import Book, BookUpdate


books_router = APIRouter()

# simple in-memory storage that mimics persistence for demo purposes
books: list[dict[str, Any]] = []


@books_router.get("/", response_model=List[Book])
async def get_all_books() -> List[Book]:
    return books


@books_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Book) -> Book:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book


@books_router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int) -> Book:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id {book_id} not found",
    )


@books_router.patch("/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update_data: BookUpdate) -> Book:
    for book in books:
        if book["id"] == book_id:
            update_payload = book_update_data.model_dump(exclude_none=True)
            if not update_payload:
                return book
            book.update(update_payload)
            book["updated_at"] = datetime.utcnow()
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id {book_id} not found",
    )


@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int) -> None:
    for idx, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(idx)
            return None
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id {book_id} not found",
    )
