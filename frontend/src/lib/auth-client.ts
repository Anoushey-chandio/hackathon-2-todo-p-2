'use client';

import { useState, useEffect, useCallback, useContext, createContext, ReactNode } from 'react';

/**
 * Authentication client for Todo App
 * Communicates with FastAPI backend via Next.js API rewrites
 * Handles JWT token management and localStorage persistence
 */

const API_BASE = "/api";

export interface User {
  id: string;
  email: string;
  name: string;
  image: string | null;
  emailVerified: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface AuthResponse {
  session: {
    access_token: string;
    token_type: string;
    expires_in?: number;
  };
  user: User;
}

export interface ErrorResponse {
  detail?: string;
  message?: string;
}

export interface SessionData {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: Error | null;
}

/**
 * Sign up new user
 */
export async function signUp(
  email: string,
  password: string,
  name: string
): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE}/auth/sign-up`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, name }),
  });

  if (!response.ok) {
    const error = (await response.json()) as ErrorResponse;
    throw new Error(error.detail || error.message || "Sign up failed");
  }

  const data = (await response.json()) as AuthResponse;
  
  // Store token
  if (data.session?.access_token) {
    localStorage.setItem("auth_token", data.session.access_token);
    localStorage.setItem("user", JSON.stringify(data.user));
    // Set cookie for middleware
    document.cookie = `token=${data.session.access_token}; path=/; max-age=3600; SameSite=Lax`;
  }

  return data;
}

/**
 * Sign in user
 */
export async function signIn(
  email: string,
  password: string
): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE}/auth/sign-in`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = (await response.json()) as ErrorResponse;
    throw new Error(error.detail || error.message || "Sign in failed");
  }

  const data = (await response.json()) as AuthResponse;
  
  // Store token
  if (data.session?.access_token) {
    localStorage.setItem("auth_token", data.session.access_token);
    localStorage.setItem("user", JSON.stringify(data.user));
    // Set cookie for middleware
    document.cookie = `token=${data.session.access_token}; path=/; max-age=3600; SameSite=Lax`;
  }

  return data;
}

/**
 * Get current session/user info
 */
export async function getSession(): Promise<AuthResponse | null> {
  const token = localStorage.getItem("auth_token");
  
  if (!token) {
    return null;
  }

  try {
    const response = await fetch(`${API_BASE}/auth/session`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      // Token expired or invalid
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user");
      document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
      return null;
    }

    return (await response.json()) as AuthResponse;
  } catch {
    return null;
  }
}

/**
 * Sign out user
 */
export async function signOut(): Promise<void> {
  try {
    await fetch(`${API_BASE}/auth/sign-out`, {
      method: "POST",
    });
  } catch {
    // Ignore errors on sign out
  }

  // Clear local storage and cookies
  localStorage.removeItem("auth_token");
  localStorage.removeItem("user");
  document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
}

/**
 * Get current auth token
 */
export function getToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }
  return localStorage.getItem("auth_token");
}

/**
 * Get current user
 */
export function getUser(): User | null {
  if (typeof window === "undefined") {
    return null;
  }
  
  const user = localStorage.getItem("user");
  if (!user) {
    return null;
  }

  try {
    return JSON.parse(user) as User;
  } catch {
    return null;
  }
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated(): boolean {
  if (typeof window === "undefined") {
    return false;
  }
  return !!localStorage.getItem("auth_token");
}

/**
 * Add auth token to request headers
 */
export function getAuthHeaders(): Record<string, string> {
  const token = getToken();
  if (!token) {
    return {};
  }
  return {
    Authorization: `Bearer ${token}`,
  };
}

/**
 * Hook to use session
 * Returns { user, token, isLoading, error }
 */
export function useSession(): SessionData {
  const [session, setSession] = useState<SessionData>({
    user: null,
    token: null,
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    const loadSession = async () => {
      try {
        const token = getToken();
        const user = getUser();

        if (token && user) {
          // Verify token is still valid
          const response = await getSession();
          if (response) {
            setSession({
              user: response.user,
              token: response.session.access_token,
              isLoading: false,
              error: null,
            });
          } else {
            // Token invalid
            setSession({
              user: null,
              token: null,
              isLoading: false,
              error: null,
            });
          }
        } else {
          setSession({
            user: null,
            token: null,
            isLoading: false,
            error: null,
          });
        }
      } catch (err) {
        setSession({
          user: null,
          token: null,
          isLoading: false,
          error: err instanceof Error ? err : new Error("Unknown error"),
        });
      }
    };

    loadSession();
  }, []);

  return session;
}
