'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { signIn } from '@/lib/auth-client';
import { sessionManager, useSession } from '@/lib/session';
import Image from 'next/image';
import Link from 'next/link';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const router = useRouter();
  const { user, isLoading: sessionLoading } = useSession();

  // If user is already logged in, redirect to tasks page
  useEffect(() => {
    if (!sessionLoading && user) {
      router.replace('/tasks');
    }
  }, [user, sessionLoading, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await signIn(email, password);

      // Verify session updated in manager
      if (!sessionManager.getUser()) {
        throw new Error('Session verification failed. Please try again.');
      }

      // Redirect to tasks/dashboard
      router.replace('/tasks');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Sign in failed');
    } finally {
      setLoading(false);
    }
  };

  if (sessionLoading) return null; // show nothing while session is loading

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-6 bg-white dark:bg-black text-black dark:text-white font-sans">
      <Image 
        src="/assets/auth-illustration.svg" 
        alt="Authentication" 
        width={200} 
        height={200} 
        className="mb-8"
        priority
      />
      <h1 className="text-4xl font-bold mb-6 text-light-purple tracking-tight">Welcome Back</h1>
      {error && <p className="text-red-500 mb-4 bg-red-50 p-2 rounded border border-red-200">{error}</p>}
      <form onSubmit={handleSubmit} className="w-full max-w-sm flex flex-col gap-4">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="p-3 border-2 rounded-xl border-gray-200 focus:border-light-purple outline-none transition-all dark:bg-gray-800 dark:border-gray-700"
          required
          disabled={loading}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="p-3 border-2 rounded-xl border-gray-200 focus:border-light-purple outline-none transition-all dark:bg-gray-800 dark:border-gray-700"
          required
          disabled={loading}
        />
        <button 
          type="submit" 
          className="p-3 bg-white text-gray-700 border-2 border-gray-100 rounded-xl font-bold hover:scale-[1.02] active:scale-[0.98] transition-all shadow-lg shadow-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={loading}
        >
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>
      <p className="text-gray-500 dark:text-gray-400 mt-6">
        Don&apos;t have an account?{' '}
        <Link href="/signup" className="text-light-purple font-semibold hover:underline">
          Sign up
        </Link>
      </p>
    </div>
  );
}
