from sqlmodel.ext.asyncio.session import AsyncSession
from .models import Book
from .schemas import BookCreate, BookUpdate
from sqlmodel import select, desc
from uuid import UUID



class BookService:


    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.execute(statement)
        return result.scalars().all()
         

    async def get_book_by_uid(self, session: AsyncSession, book_uid: UUID):
        statement = select(Book).where(Book.id == book_uid)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def create_book(self, book_data: BookCreate, session: AsyncSession):
        new_book = Book(**book_data.model_dump())
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book


    async def update_book(self, uid: UUID, update_data: BookUpdate, session: AsyncSession):
        book_to_update = await self.get_book_by_uid(session, uid)
        if book_to_update is not None:
            update_data_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_data_dict.items():
                setattr(book_to_update, key, value)
            await session.commit()
            await session.refresh(book_to_update)
            return book_to_update
        else:
            return None
          
    async def delete_book(self, session: AsyncSession, uid: UUID):
        book_to_delete = await self.get_book_by_uid(session, uid)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return True
        else:
            return False
