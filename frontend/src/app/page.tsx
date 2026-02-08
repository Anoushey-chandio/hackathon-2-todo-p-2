'use client'; // MUST be top

import Link from 'next/link';
import { useSession } from '@/lib/session';

export default function HomePage() {
  const { user, isLoading } = useSession();

  // Show nothing until session finishes loading (to prevent flickering)
  if (isLoading) return null;

  return (
    <div className="flex flex-col items-center justify-center p-6 text-center min-h-[calc(100vh-64px)] bg-white dark:bg-black text-black dark:text-white">
      <div className="max-w-3xl mt-12 md:mt-20">
        <h1 className="text-5xl md:text-7xl font-extrabold mb-6 tracking-tight text-gray-900 dark:text-white leading-tight">
          Organize your{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-light-purple to-light-cyan">
            chaos
          </span>
          .
        </h1>
        <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-400 mb-10 max-w-2xl mx-auto leading-relaxed">
          The simple, secure, and beautiful way to manage your tasks.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
          {!user ? (
            <>
              {/* ✅ Not Logged In: Show Sign Up & Sign In */}
              <Link
                href="/signup"
                className="px-8 py-4 bg-light-purple text-white text-lg font-bold rounded-2xl hover:bg-opacity-90 hover:scale-105 transition-all shadow-lg shadow-purple-200 dark:shadow-purple-900/20"
              >
                Get Started Free
              </Link>
              <Link
                href="/signin"
                className="px-8 py-4 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 border-2 border-gray-100 dark:border-gray-700 text-lg font-bold rounded-2xl hover:border-light-purple dark:hover:border-light-purple transition-all"
              >
                Log In
              </Link>
            </>
          ) : (
            <>
              {/* ✅ Logged In: Show Go to Tasks button instead of redirecting */}
              <div className="flex flex-col items-center gap-4">
                <p className="text-gray-600 dark:text-gray-400 text-lg">
                  Welcome back, <span className="font-bold text-light-purple">{user.name || 'User'}</span>!
                </p>
                <Link
                  href="/tasks"
                  className="px-10 py-4 bg-light-purple text-white text-lg font-bold rounded-2xl hover:bg-opacity-90 hover:scale-105 transition-all shadow-lg shadow-purple-200 dark:shadow-purple-900/20"
                >
                  Go to My Tasks
                </Link>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}