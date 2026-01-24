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
    // Wait until session check finishes
    if (isLoading) return;

    // 🚫 Not logged in + protected route → go to signin
    if (!user && isProtectedRoute) {
      router.replace('/signin');
      return;
    }

    // ✅ Logged in + auth pages → go to tasks
    if (user && isAuthRoute) {
      router.replace('/tasks');
      return;
    }
  }, [user, isLoading, pathname, router]);

  // ⏳ Loading spinner ONLY for protected routes
  if (isLoading && isProtectedRoute) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  // 🚫 Prevent protected content flash
  if (!isLoading && !user && isProtectedRoute) {
    return null;
  }

  return <>{children}</>;
}
