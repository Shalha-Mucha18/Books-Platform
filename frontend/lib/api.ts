export type Book = {
  id: string;
  title: string;
  author: string;
  publisher: string;
  published_date: string;
  page_count: number;
  language: string;
  created_at: string;
  updated_at: string;
  user_uid?: string | null;
};

const fallbackBooks: Book[] = [
  {
    id: "demo-001",
    title: "Designing Fast APIs",
    author: "Tech Core Team",
    publisher: "Books Platform",
    published_date: "2023-10-01",
    page_count: 288,
    language: "en",
    created_at: "2023-10-01T00:00:00Z",
    updated_at: "2023-10-01T00:00:00Z",
    user_uid: null
  },
  {
    id: "demo-002",
    title: "Async Python Patterns",
    author: "Ops Guild",
    publisher: "Books Platform",
    published_date: "2023-06-15",
    page_count: 352,
    language: "en",
    created_at: "2023-06-15T00:00:00Z",
    updated_at: "2023-07-11T00:00:00Z",
    user_uid: null
  },
  {
    id: "demo-003",
    title: "Scaling Book Reviews",
    author: "Data Chapter",
    publisher: "Books Platform",
    published_date: "2024-01-20",
    page_count: 240,
    language: "en",
    created_at: "2024-01-20T00:00:00Z",
    updated_at: "2024-02-02T00:00:00Z",
    user_uid: null
  }
];

type FetchBooksResult = {
  books: Book[];
  error?: string;
};

export async function fetchBooks(): Promise<FetchBooksResult> {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1.0.0";
  const accessToken = process.env.NEXT_PUBLIC_API_ACCESS_TOKEN;

  try {
    const response = await fetch(`${baseUrl}/books/`, {
      headers: {
        "Content-Type": "application/json",
        ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {})
      },
      cache: "no-store",
      next: { revalidate: 30 }
    });

    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }

    const books = (await response.json()) as Book[];
    return { books };
  } catch (error) {
    const message =
      error instanceof Error ? error.message : "Unable to reach the Books API";
    return {
      books: fallbackBooks,
      error: `${message}. Showing curated sample data instead.`
    };
  }
}
