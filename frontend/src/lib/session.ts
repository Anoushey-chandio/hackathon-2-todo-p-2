// Custom session management for Python backend
// This replaces better-auth's session management

export interface User {
  id: string;
  email: string;
  name: string;
  image?: string;
  emailVerified: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Session {
  id: string;
  userId: string;
  token: string;
  expiresAt: string;
  createdAt: string;
  updatedAt: string;
}

export interface SessionData {
  user: User;
  session: Session;
}

class SessionManager {
  private sessionData: SessionData | null = null;
  private listeners: Set<(session: SessionData | null) => void> = new Set();

  async getSession(): Promise<SessionData | null> {
    // Try to get from cache first
    if (this.sessionData) {
      return this.sessionData;
    }

    // Try to get from backend
    try {
      const response = await fetch('/api/auth/session', {
        method: 'GET',
        credentials: 'include',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
        },
      });

      if (response.ok) {
        this.sessionData = await response.json();
        this.notifyListeners(this.sessionData);
        return this.sessionData;
      } else if (response.status === 401) {
        // Not logged in
        this.sessionData = null;
        this.notifyListeners(null);
        return null;
      }
    } catch (error) {
      console.error('Failed to fetch session:', error);
    }

    return null;
  }

  setSession(session: SessionData | null): void {
    this.sessionData = session;
    if (session?.session?.token) {
      localStorage.setItem('auth_token', session.session.token);
      document.cookie = `token=${session.session.token}; path=/; max-age=3600; SameSite=Lax`;
    } else {
      localStorage.removeItem('auth_token');
      document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    }
    this.notifyListeners(session);
  }

  clearSession(): void {
    this.sessionData = null;
    localStorage.removeItem('auth_token');
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    this.notifyListeners(null);
  }

  subscribe(listener: (session: SessionData | null) => void): () => void {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private notifyListeners(session: SessionData | null): void {
    this.listeners.forEach(listener => listener(session));
  }
}

export const sessionManager = new SessionManager();
