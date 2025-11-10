from datetime import datetime
from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .schemas import Book, BookCreate, BookUpdate
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .service import BookService


books_router = APIRouter()
book_service = BookService()



@books_router.get("/", response_model=List[Book])
async def get_all_books(session:AsyncSession = Depends(get_session) ) -> List[Book]:
    all_book = await book_service.get_all_books(session)
    return all_book


@books_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreate, session: AsyncSession = Depends(get_session)) -> Book:
    new_book = await book_service.create_book(book_data, session)
    return new_book


@books_router.get("/{book_id}", response_model=Book)
async def get_book(book_id: UUID, session:AsyncSession = Depends(get_session) ) -> Book:
    book = await book_service.get_book_by_uid(session, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return book

@books_router.patch("/{book_id}", response_model=Book)
async def update_book(book_id: UUID, book_update_data: BookUpdate, session:AsyncSession = Depends(get_session) ) -> Book:
    updated_book = await book_service.update_book(book_id, book_update_data, session)
    if updated_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return updated_book


@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID,session:AsyncSession = Depends(get_session) ) -> None:
    success = await book_service.delete_book(session, book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return None
