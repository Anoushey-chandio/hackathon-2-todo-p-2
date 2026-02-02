import { fetchClient } from './api';
import { sessionManager } from './session';

export interface AuthResponse {
  user: any;
}

export interface ErrorResponse {
  detail?: string;
  message?: string;
}

// --------------------
// Sign Up
export async function signUp(email: string, password: string, name?: string) {
  const res = await fetchClient('/api/auth/sign-up', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, name }),
    credentials: 'include', // ✅ cookies ke liye
  });

  if (!res.ok) {
    const err = await res.json() as ErrorResponse;
    throw new Error(err.detail || err.message || 'Sign up failed');
  }

  const data = await res.json() as AuthResponse;
  sessionManager.setSession(data);
  return data;
}

// --------------------
// Sign In
export async function signIn(email: string, password: string) {
  const res = await fetchClient('/api/auth/sign-in', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
    credentials: 'include', // ✅ cookies ke liye
  });

  if (!res.ok) {
    const err = await res.json() as ErrorResponse;
    throw new Error(err.detail || err.message || 'Sign in failed');
  }

  const data = await res.json() as AuthResponse;
  sessionManager.setSession(data);
  return data;
}

// --------------------
// Sign Out
export async function signOut() {
  await fetchClient('/api/auth/sign-out', {
    method: 'POST',
    credentials: 'include', // ✅ cookies ke liye
  });
  sessionManager.clearSession();
}

// --------------------
// Get Session (READ ONLY)
export async function getSession(): Promise<AuthResponse | null> {
  const res = await fetchClient('/api/auth/session', {
    method: 'GET',
    credentials: 'include', // ✅ cookies ke liye
  });

  if (!res.ok) return null;
  const data = await res.json();
  sessionManager.setSession(data);
  return data;
}
