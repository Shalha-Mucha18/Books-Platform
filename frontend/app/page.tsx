import Link from "next/link";
import { BooksGrid } from "../components/BooksGrid";
import { fetchBooks } from "../lib/api";

export default async function Home() {
  const { books = [], error } = await fetchBooks();

  const metrics = [
    { label: "Books indexed", value: String(books.length).padStart(2, "0") },
    { label: "Avg. reviewer score", value: "4.9 / 5" },
    { label: "Uptime last 30d", value: "99.9%" },
    { label: "Latency target", value: "< 200ms" }
  ];

  const valueProps = [
    {
      title: "Audit-ready API",
      description: "Typed SQLModel entities, JWT auth, and role-aware routers for confident demos."
    },
    {
      title: "Operational insights",
      description: "Real-time catalog pulse with curated fallback data so the UI never feels empty."
    },
    {
      title: "Modern experience",
      description: "Next.js App Router, streaming server components, and polished states for every flow."
    },
    {
      title: "Frictionless handoffs",
      description: "Links to API docs, README runbooks, and infra toggles right from the hero."
    }
  ];

  return (
    <main>
      <header className="page-header">
        <span className="logo">Books Platform</span>
        <div className="nav-links">
          <Link href="/dashboard">Dashboard</Link>
          <Link href="#books">Catalog</Link>
          <Link href="#capabilities">Capabilities</Link>
          <Link href="#runbook">Runbook</Link>
          <Link href="http://localhost:8000/docs" target="_blank" rel="noreferrer">
            API Docs
          </Link>
        </div>
        <Link
          href="http://localhost:8000/api/v1.0.0/auth/login"
          className="cta-button login-button"
          target="_blank"
          rel="noreferrer"
        >
          User login
        </Link>
      </header>

      <section className="hero">
        <p className="badge">Full-stack reference</p>
        <h1>Showcase a production-ready book platform</h1>
        <p>
          Secure FastAPI services meet a refined React dashboard. Review real catalog data,
          spotlight stability metrics, and guide teammates straight to the right docs.
        </p>
        <div className="hero__cta">
          <Link href="/dashboard" className="cta-button primary">
            View dashboard
          </Link>
          <Link href="http://localhost:8000/docs" className="cta-button secondary">
            API docs
          </Link>
          <Link
            href="http://localhost:8000/api/v1.0.0/auth/login"
            className="cta-button outline"
            target="_blank"
            rel="noreferrer"
          >
            User login
          </Link>
        </div>
        <div className="hero__metrics">
          {metrics.map((metric) => (
            <div className="metric-card" key={metric.label}>
              <span>{metric.label}</span>
              <strong>{metric.value}</strong>
            </div>
          ))}
        </div>
      </section>

      <section className="quick-actions" id="quick-actions">
        <article>
          <h3>User login</h3>
          <p>Authenticate with your JWT credentials to manage your personal catalog.</p>
          <Link
            href="http://localhost:8000/api/v1.0.0/auth/login"
            className="cta-link"
            target="_blank"
            rel="noreferrer"
          >
            Go to login →
          </Link>
        </article>
        <article>
          <h3>Create account</h3>
          <p>Sign up through `/auth/signup` and grab your tokens for the dashboard.</p>
          <Link
            href="http://localhost:8000/api/v1.0.0/auth/signup"
            className="cta-link"
            target="_blank"
            rel="noreferrer"
          >
            Create user →
          </Link>
        </article>
        <article>
          <h3>Docs & runbook</h3>
          <p>Follow the README instructions to run FastAPI + Next.js locally.</p>
          <Link href="#runbook" className="cta-link">
            See runbook →
          </Link>
        </article>
      </section>

      <section className="value-section" id="capabilities">
        <div className="section-heading">
          <h2>Platform capabilities</h2>
          <p className="text-subtle">
            Built for product walkthroughs: resilience, transparency, and actionable CTAs.
          </p>
        </div>
        <div className="value-grid">
          {valueProps.map((value) => (
            <article className="value-card" key={value.title}>
              <h3>{value.title}</h3>
              <p>{value.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="books-section" id="books">
        <div className="section-heading">
          <h2>Latest imports</h2>
          <p>Synced live from the FastAPI service. Tokens optional for demo mode.</p>
        </div>
        {error ? <div className="alert">{error}</div> : null}
        <BooksGrid books={books} />
      </section>

      <section className="cta-panel" id="runbook">
        <h2>Ready to run it live?</h2>
        <p>
          Start the FastAPI backend (`uvicorn src:app --reload`) and the Next.js dashboard
          (`npm run dev`) to reproduce the full experience locally.
        </p>
        <div className="cta-panel__actions">
          <Link href="http://localhost:8000/docs" className="cta-button primary">
            Start API
          </Link>
          <Link
            href="https://fastapi.tiangolo.com"
            className="cta-button secondary"
            target="_blank"
            rel="noreferrer"
          >
            FastAPI guide
          </Link>
        </div>
      </section>
    </main>
  );
}
