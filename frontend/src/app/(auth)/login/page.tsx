'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { fetchClient } from '@/lib/api';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const res = await fetchClient('/auth/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData,
      });

      if (!res.ok) {
        throw new Error('Invalid credentials');
      }

      const data = await res.json();
      const token = data.access_token;

      // Store in localStorage for API calls
      localStorage.setItem('token', token);
      // Store in cookie for Middleware
      document.cookie = `token=${token}; path=/; max-age=1800; SameSite=Lax`;

      router.push('/');
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-6 bg-white dark:bg-black text-black dark:text-white">
      <h1 className="text-3xl font-bold mb-6 text-light-purple">Login</h1>
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
          Sign In
        </button>
      </form>
      <p className="mt-4">
        Don't have an account? <a href="/signup" className="text-light-cyan hover:underline">Sign up</a>
      </p>
    </div>
  );
}
