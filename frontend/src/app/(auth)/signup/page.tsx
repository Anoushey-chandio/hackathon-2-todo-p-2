'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { signUp } from '@/lib/auth-client';
import Image from 'next/image';

export default function SignupPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await signUp(email, password, username);
      // Redirect to dashboard on success
      router.push('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Sign up failed');
    } finally {
      setLoading(false);
    }
  };

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
      <h1 className="text-4xl font-bold mb-6 text-light-purple tracking-tight">Create Account</h1>
      {error && <p className="text-red-500 mb-4 bg-red-50 p-2 rounded border border-red-200">{error}</p>}
      <form onSubmit={handleSubmit} className="w-full max-w-sm flex flex-col gap-4">
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="p-3 border-2 rounded-xl border-gray-200 focus:border-light-purple outline-none transition-all dark:bg-gray-800 dark:border-gray-700"
          required
          disabled={loading}
        />
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
          {loading ? 'Signing up...' : 'Sign Up'}
        </button>
      </form>
    </div>
  );
}
