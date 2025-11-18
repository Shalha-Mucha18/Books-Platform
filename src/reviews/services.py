from uuid import UUID

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.service import UserService
from src.books.service import BookService
from src.db.models import Review
from .schemas import ReviewCreateModel

book_service = BookService()
user_service = UserService()



class ReviewService:
    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        book = await book_service.get_book_by_uid(session, UUID(book_uid))
        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )

        user = await user_service.get_user_by_email(email=user_email, session=session)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        review_payload = review_data.model_dump()
        new_review = Review(**review_payload)
        new_review.user = user
        new_review.book = book

        session.add(new_review)
        await session.commit()
        await session.refresh(new_review)
        return new_review
