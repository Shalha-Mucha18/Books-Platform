from fastapi import FastAPI
from src.books.routers import books_router


version = 'v1.0.0'


app = FastAPI(
    version=version,
    title="Books API",
    description="An API to manage books",   
)

app.include_router(books_router,prefix = f"/api/{version}/books", tags = ['books'])
