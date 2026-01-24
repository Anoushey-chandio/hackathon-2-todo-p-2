import { useEffect, useState } from 'react';
import { fetchClient } from './api';

export interface User {
  id: string;
  email: string;
  name: string;
  image?: string;
  emailVerified: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface SessionData {
  user: User;
}

type Listener = (session: SessionData | null) => void;

class SessionManager {
  private session: SessionData | null = null;
  private listeners = new Set<Listener>();
  private loadingPromise: Promise<SessionData | null> | null = null;

  // 🔐 single fetch guard
  async getSession(): Promise<SessionData | null> {
    if (this.session) return this.session;
    if (this.loadingPromise) return this.loadingPromise;

    this.loadingPromise = fetchClient('/api/auth/session', {
      method: 'GET',
    })
      .then(async res => {
        if (!res.ok) return null;
        const data = await res.json();
        this.setSession(data);
        return data;
      })
      .finally(() => {
        this.loadingPromise = null;
      });

    return this.loadingPromise;
  }

  setSession(session: SessionData | null) {
    this.session = session;
    this.listeners.forEach(fn => fn(session));
  }

  clearSession() {
    this.setSession(null);
  }

  subscribe(listener: Listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  getUser() {
    return this.session?.user ?? null;
  }
}

export const sessionManager = new SessionManager();

// --------------------
// React Hook
export function useSession() {
  const [session, setSession] = useState<SessionData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    sessionManager.getSession().then(s => {
      if (mounted) {
        setSession(s);
        setLoading(false);
      }
    });

    const unsubscribe = sessionManager.subscribe(s => {
      if (mounted) setSession(s);
    });

    return () => {
      mounted = false;
      unsubscribe();
    };
  }, []);

  return {
    session,
    user: session?.user ?? null,
    isLoading: loading,
  };
}
