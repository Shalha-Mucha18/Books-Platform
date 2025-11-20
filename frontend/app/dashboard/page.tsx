import Link from "next/link";
import { fetchBooks, type Book } from "../../lib/api";

const formatNumber = (value: number) => new Intl.NumberFormat("en-US").format(value);
const formatDate = (iso: string) =>
  new Date(iso).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric"
  });

function getTopLanguages(books: Book[]) {
  const map = new Map<string, number>();
  books.forEach((book) => {
    const lang = book.language.toUpperCase();
    map.set(lang, (map.get(lang) ?? 0) + 1);
  });
  return Array.from(map.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3);
}

function getRecentBooks(books: Book[]) {
  return [...books]
    .sort(
      (a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
    )
    .slice(0, 6);
}

export default async function Dashboard() {
  const { books = [], error } = await fetchBooks();

  const totalPages = books.reduce((sum, book) => sum + (book.page_count ?? 0), 0);
  const avgPages = books.length ? Math.round(totalPages / books.length) : 0;
  const languages = getTopLanguages(books);
  const recentBooks = getRecentBooks(books);

  const stats = [
    { label: "Books indexed", value: formatNumber(books.length), meta: "live" },
    { label: "Avg. page count", value: `${avgPages} pages`, meta: "per title" },
    {
      label: "Languages",
      value: languages.length ? languages[0][0] : "N/A",
      meta: `${languages.reduce((sum, [, count]) => sum + count, 0)} tracked`
    },
    { label: "Total pages", value: formatNumber(totalPages), meta: "library-wide" }
  ];

  const insights = [
    {
      title: "Catalog freshness",
      detail: recentBooks.length
        ? `Updated ${formatDate(recentBooks[0].updated_at)}`
        : "Awaiting first sync",
      trend: "+2 titles this week"
    },
    {
      title: "Auth coverage",
      detail: "JWT, RBAC, refresh tokens",
      trend: "Access tokens valid 15 min"
    },
    {
      title: "Operational status",
      detail: "PostgreSQL + Redis healthy",
      trend: "99.9% uptime target"
    }
  ];

  return (
    <main className="dashboard">
      <section className="dashboard-hero">
        <div>
          <p className="badge">Operations view</p>
          <h1>Books Platform dashboard</h1>
          <p>
            Track catalog metrics, inspect recent imports, and jump directly into the FastAPI
            runbook when something needs attention.
          </p>
        </div>
        <div className="dashboard-cta">
          <Link href="/" className="cta-button secondary">
            Back to marketing
          </Link>
          <Link href="http://localhost:8000/docs" className="cta-button primary">
            Open API docs
          </Link>
        </div>
      </section>

      <section className="stats-grid">
        {stats.map((stat) => (
          <article className="stat-card" key={stat.label}>
            <span>{stat.label}</span>
            <strong>{stat.value}</strong>
            <p>{stat.meta}</p>
          </article>
        ))}
      </section>

      <section className="insights-grid">
        {insights.map((insight) => (
          <article className="insight-card" key={insight.title}>
            <p className="insight-title">{insight.title}</p>
            <h3>{insight.detail}</h3>
            <span className="trend">{insight.trend}</span>
          </article>
        ))}
      </section>

      <section className="table-section">
        <div className="section-heading">
          <h2>Recent book activity</h2>
          <p className="text-subtle">
            Last six updates from the FastAPI catalog. Use tokens for live data; otherwise demo
            entries remain visible.
          </p>
        </div>
        {error ? <div className="alert">{error}</div> : null}
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Author</th>
                <th>Publisher</th>
                <th>Language</th>
                <th>Updated</th>
              </tr>
            </thead>
            <tbody>
              {recentBooks.map((book) => (
                <tr key={book.id}>
                  <td>{book.title}</td>
                  <td>{book.author}</td>
                  <td>{book.publisher}</td>
                  <td>{book.language.toUpperCase()}</td>
                  <td>{formatDate(book.updated_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {!recentBooks.length ? (
            <p className="text-subtle">No activity yet. Add books via the API to populate.</p>
          ) : null}
        </div>
      </section>

      <section className="activity-feed">
        <div className="section-heading">
          <h2>Activity feed</h2>
          <p className="text-subtle">Derived from latest writes inside the Books service.</p>
        </div>
        <ul>
          {recentBooks.map((book) => (
            <li key={`${book.id}-activity`}>
              <div>
                <strong>{book.title}</strong>
                <span> by {book.author}</span>
              </div>
              <span>{formatDate(book.created_at)}</span>
            </li>
          ))}
          {!recentBooks.length ? <li>No events yet.</li> : null}
        </ul>
      </section>
    </main>
  );
}
