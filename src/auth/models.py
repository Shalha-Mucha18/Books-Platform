from sqlmodel import SQLModel
import uuid
from sqlmodel import Field
from sqlalchemy import Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime

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

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
