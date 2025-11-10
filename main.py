dfrom fastapi import FastAPI, status
from src.books.schemas import Book, BookUpdate
from fastapi.exceptions import HTTPException

app = FastAPI()

books=[]




if __name__ == "__main__":
    main()
