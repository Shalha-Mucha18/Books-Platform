import Link from "next/link";
import type { Book } from "../lib/api";

const formatDate = (value: string) =>
  new Date(value).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric"
  });

export function BookCard({ book }: { book: Book }) {
  const inspectUrl = `http://localhost:8000/api/v1.0.0/books/${book.id}`;
  const ownerLabel = book.user_uid ? `User ${book.user_uid.slice(0, 8)}` : "Service import";

  return (
    <article className="book-card">
      <header>
        <div>
          <div className="badge">{book.language.toUpperCase()}</div>
          <h3>{book.title}</h3>
          <span>by {book.author}</span>
        </div>
        <span className="tag">{book.page_count} pages</span>
      </header>
      <p className="book-description">
        {book.publisher} · Published {formatDate(book.published_date)}
      </p>
      <div className="book-meta">
        <span>
          Owner: <strong>{ownerLabel}</strong>
        </span>
        <span>
          Added: <strong>{formatDate(book.created_at)}</strong>
        </span>
      </div>
      <footer className="book-footer">
        <span>Updated {formatDate(book.updated_at)}</span>
        <Link href={inspectUrl} className="book-link" target="_blank" rel="noreferrer">
          Inspect record →
        </Link>
      </footer>
    </article>
  );
}
