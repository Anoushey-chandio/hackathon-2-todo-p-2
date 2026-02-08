'use client';

import { useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useSession } from '@/lib/session';

export default function AuthGuard({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const { user, isLoading } = useSession();

  const isProtectedRoute = pathname.startsWith('/tasks');
  const isAuthRoute = pathname === '/signin' || pathname === '/signup';

  useEffect(() => {
    // Wait for session to load
    if (isLoading) return;

    // 1️⃣ User not logged in + trying protected route → redirect to signin
    if (!user && isProtectedRoute) {
      router.replace('/signin');
      return;
    }

    // 2️⃣ User logged in + on signin/signup → redirect to tasks
    if (user && isAuthRoute) {
      router.replace('/tasks');
      return;
    }

    // 3️⃣ Logged-in user on other pages → do nothing
  }, [user, isLoading, pathname, router]);

  // ⏳ Show loader for protected routes while checking session
  if (isLoading && isProtectedRoute) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  // 🚫 Prevent flash of protected content for logged-out users
  if (!isLoading && !user && isProtectedRoute) {
    return null;
  }

  return <>{children}</>;
}
