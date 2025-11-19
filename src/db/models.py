import uuid
from datetime import datetime, date
from typing import Optional
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel
from typing import List

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        sa_column=Column(  
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4, 
        )
    )
    username: str = Field(index=True, nullable=False, unique=True)
    email: str 
    first_name: str | None = Field(default=None, nullable=True)
    last_name: str | None = Field(default=None, nullable=True)
    password_hash: str = Field(exclude=True, nullable=False)
    role: str = Field(
        sa_column = Column(pg.VARCHAR, nullable=False, server_default='user')
    )
    is_verified: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    reviews: List["Review"] = Relationship(back_populates="user")
    books: List["Book"] = Relationship(back_populates="user")


    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"

class Book(SQLModel, table=True):
    __tablename__ = "books"  

    id: uuid.UUID = Field(
        sa_column=Column(  
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4, 
        )
    )

    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow, 
        )
    )

    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow,
            onupdate=datetime.utcnow
        )
    )
    user: Optional['User'] = Relationship(back_populates='books')
    reviews: List['Review'] = Relationship(back_populates='book')


    def __repr__(self):
        return (
            f"Book(title={self.title}, author={self.author}, "
            f"publisher={self.publisher}, published_date={self.published_date}, "
            f"page_count={self.page_count}, language={self.language}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )

class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    rating: int = Field(ge=1, le=5)
    review_text: str

    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.id")

    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow,
            onupdate=datetime.utcnow
        )
    )

    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"
