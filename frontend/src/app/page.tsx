'use client';

import Link from 'next/link';
import Image from 'next/image';
import { authClient } from '@/lib/auth-client';

export default function WelcomePage() {
  const { data: session } = authClient.useSession();

  return (
    <div className="flex flex-col items-center justify-center p-6 text-center animate-in fade-in duration-700 min-h-[calc(100vh-64px)]">
      
      {/* Hero Section */}
      <div className="max-w-3xl mt-12 md:mt-20">
        <h1 className="text-5xl md:text-7xl font-extrabold mb-6 tracking-tight text-gray-900 dark:text-white leading-tight">
          Organize your <span className="text-transparent bg-clip-text bg-gradient-to-r from-light-purple to-light-cyan">chaos</span>.
        </h1>
        <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-400 mb-10 max-w-2xl mx-auto leading-relaxed">
          The simple, secure, and beautiful way to manage your tasks.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
          {session ? (
            <Link 
              href="/tasks" 
              className="px-8 py-4 bg-gray-900 dark:bg-white text-white dark:text-gray-900 text-lg font-bold rounded-2xl hover:scale-105 transition-transform shadow-xl"
            >
              Go to Dashboard
            </Link>
          ) : (
            <>
                <Link 
                href="/signup" 
                className="px-8 py-4 bg-light-purple text-white text-lg font-bold rounded-2xl hover:bg-opacity-90 hover:scale-105 transition-all shadow-lg shadow-purple-200 dark:shadow-purple-900/20"
                >
                Get Started Free
                </Link>
                <Link 
                href="/login" 
                className="px-8 py-4 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 border-2 border-gray-100 dark:border-gray-700 text-lg font-bold rounded-2xl hover:border-light-purple dark:hover:border-light-purple transition-all"
                >
                Log In
                </Link>
            </>
          )}
        </div>
      </div>

      {/* Illustration */}
      <div className="relative w-full max-w-4xl mx-auto hidden md:block">
        <div className="absolute top-0 -left-4 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute top-0 -right-4 w-72 h-72 bg-cyan-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
        <div className="relative">
            <Image 
            src="/assets/tasks-illustration.svg" 
            alt="App Preview" 
            width={600} 
            height={400}
            className="mx-auto drop-shadow-2xl hover:scale-105 transition-transform duration-500 w-auto h-auto"
            priority
            />
        </div>
      </div>
    </div>
  );
}
