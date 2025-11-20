import type { Book } from "../lib/api";
import { BookCard } from "./BookCard";

export function BooksGrid({ books }: { books: Book[] }) {
  if (!books.length) {
    return (
      <div className="empty-state">
        <h3>No books yet</h3>
        <p>POST a book to `/api/v1.0.0/books/` and refresh to watch it appear instantly.</p>
        <code>curl -X POST http://localhost:8000/api/v1.0.0/books/ ...</code>
      </div>
    );
  }

  return (
    <div className="books-grid">
      {books.map((book) => (
        <BookCard key={book.id} book={book} />
      ))}
    </div>
  );
}
