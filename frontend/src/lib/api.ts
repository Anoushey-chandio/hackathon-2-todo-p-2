'use client';

import { sessionManager } from '@/lib/session';

// FastAPI backend base URL
const API_URL = 'https://anoushey-full-stack-todo-chatbot.hf.space';

export async function fetchClient(
  path: string,
  options: RequestInit = {},
  query?: Record<string, string | number | boolean | undefined>
): Promise<Response> {
  // Ensure leading slash
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;

  const url = new URL(`${API_URL}${normalizedPath}`);

  // Append query parameters
  if (query) {
    Object.entries(query).forEach(([key, value]) => {
      if (value !== undefined) url.searchParams.append(key, String(value));
    });
  }

  const headers = new Headers(options.headers);

  if (options.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  headers.set('X-Requested-With', 'XMLHttpRequest');

  const fetchOptions: RequestInit = {
    ...options,
    headers,
    credentials: 'include', // send cookies automatically
  };

    try {
      const res = await fetch(url.toString(), fetchOptions);

      // Handle 401 globally for non-auth routes
      if (res.status === 401 && !normalizedPath.startsWith('/api/auth')) {
        console.warn('Received 401 - clearing session and redirecting');
        sessionManager.clearSession();
        if (typeof window !== 'undefined') {
          window.location.href = '/signin';
        }
      }

      return res;
  } catch (error) {
    console.error('API fetch failed:', error);
    return new Response(JSON.stringify({ detail: 'Network error' }), { status: 500 });
  }
}
