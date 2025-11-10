from fastapi import FastAPI
from src.books.routers import books_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_db()
    yield
    print("Shutting down...")  


version = 'v1.0.0'


app = FastAPI(
    version=version,
    title="Books API",
    description="An API to manage books",   
    lifespan=lifespan
)

app.include_router(books_router,prefix = f"/api/{version}/books", tags = ['books'])
