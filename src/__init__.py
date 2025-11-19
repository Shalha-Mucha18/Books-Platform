from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.books.routers import books_router
from src.error import register_all_errors
from src.auth.routers import auth_router
from src.reviews.routers import review_router
from src.db.main import init_db
from .middleware import register_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    from src.db.models import Book
    await init_db()
    yield
    print("Shutting down...")  


version = 'v1.0.0'


app = FastAPI(
    version=version,
    title="Books API",
    description="An API to manage books" 

)

register_all_errors(app)
register_middleware(app)


app.include_router(books_router,prefix = f"/api/{version}/books", tags = ['books'])
app.include_router(auth_router,prefix = f"/api/{version}/auth", tags = ['auth'])
app.include_router(review_router,prefix = f"/api/{version}/review", tags = ['review'])
