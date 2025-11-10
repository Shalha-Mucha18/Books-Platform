from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
import uuid
from pydantic import BaseModel

class Book(SQLModel, table=True):
    __tablename__ = "books"  # Explicit table name

    id: uuid.UUID = Field(
        sa_column=Column(  # ✅ "Column", not "CLoumn"
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,  # ✅ pass the function, not call it
        )
    )

    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str

    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow,  # ✅ pass function, not call
        )
    )

    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow,
            onupdate=datetime.utcnow
        )
    )

    def __repr__(self):
        return (
            f"Book(title={self.title}, author={self.author}, "
            f"publisher={self.publisher}, published_date={self.published_date}, "
            f"page_count={self.page_count}, language={self.language}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )
