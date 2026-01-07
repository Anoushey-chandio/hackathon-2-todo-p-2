'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { fetchClient } from '@/lib/api';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const res = await fetchClient('/auth/signup', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Signup failed');
      }

      router.push('/login');
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-6 bg-white dark:bg-black text-black dark:text-white">
      <h1 className="text-3xl font-bold mb-6 text-light-purple">Sign Up</h1>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="w-full max-w-sm flex flex-col gap-4">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="p-3 border rounded border-gray-300"
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="p-3 border rounded border-gray-300"
          required
        />
        <button type="submit" className="p-3 bg-light-purple text-white rounded hover:bg-opacity-90">
          Create Account
        </button>
      </form>
      <p className="mt-4">
        Already have an account? <a href="/login" className="text-light-cyan hover:underline">Log in</a>
      </p>
    </div>
  );
}
