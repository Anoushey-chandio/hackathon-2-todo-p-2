// This route handler should NOT exist.
// Authentication is handled ONLY by the FastAPI backend at http://127.0.0.1:8000/api/auth
// The next.config.ts rewrites /api/auth/* to the backend.
// This file is kept but disabled to prevent conflicts.

export const dynamic = 'force-dynamic';

export async function GET() {
  return new Response(
    JSON.stringify({ error: 'Use the Python backend API instead' }),
    { status: 404 }
  );
}

export async function POST() {
  return new Response(
    JSON.stringify({ error: 'Use the Python backend API instead' }),
    { status: 404 }
  );
}