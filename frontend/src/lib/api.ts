import { sessionManager } from '@/lib/session';

// Use the Next.js proxy path to ensure cookies are passed correctly
// The rewrite in next.config.ts maps /api/py -> http://127.0.0.1:8000/api
const API_URL = '/api/py';

export async function fetchClient(path: string, options: RequestInit = {}) {
  // Ensure path starts with a slash and strip any leading /api if present
  // This prevents double /api segments when using the proxy (e.g. /api/py/api/tasks -> /api/py/tasks)
  let normalizedPath = path.startsWith('/') ? path : `/${path}`;
  if (normalizedPath.startsWith('/api/')) {
      normalizedPath = normalizedPath.replace('/api/', '/');
  }

  const url = `${API_URL}${normalizedPath}`;

  const headers = new Headers(options.headers);

  // Set default Content-Type for requests with a body
  if (options.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  // Add headers to satisfy strict CORS/Proxy requirements
  headers.set('X-Requested-With', 'XMLHttpRequest');

  // Add Authorization Bearer Token if session exists
  // The token comes from the backend session, which is stored in a cookie
  // The backend's get_token dependency checks for Bearer token first, then the cookie
  // So we mainly rely on cookies being sent via credentials: 'include'
  // But we can also try to get the token from localStorage if it was stored
  if (typeof window !== 'undefined') {
    try {
      const storedToken = localStorage.getItem('auth_token');
      if (storedToken) {
        headers.set('Authorization', `Bearer ${storedToken}`);
      }
    } catch {
      // Ignore localStorage errors
    }
  }

  // Note: Setting Origin manually in browser `fetch` is often ignored by browsers for security,
  // but we add it here to satisfy the requirement if running in a context that allows it.
  if (!headers.has('Origin')) {
     try {
       headers.set('Origin', typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000');
     } catch {
       // Ignore if browser blocks setting Origin
     }
  }

  const fetchOptions: RequestInit = {
    ...options,
    headers,
    // We still send credentials just in case, but Bearer is primary for Python backend now
    credentials: 'include', 
  };

  try {
    const response = await fetch(url, fetchOptions);

    // Only handle 401 if it's not an auth-related request
    if (response.status === 401 && !path.includes('/auth/')) {
      if (typeof window !== 'undefined') {
        // Clear session and redirect to login
        sessionManager.clearSession();
        window.location.href = '/login';
      }
    }

    return response;
  } catch (error) {
    console.error(`Fetch error for ${url}:`, error);
    return {
      ok: false,
      status: 500,
      statusText: 'Fetch Error',
      json: async () => ({ detail: 'Network error or CORS block' }),
    } as Response;
  }
}
