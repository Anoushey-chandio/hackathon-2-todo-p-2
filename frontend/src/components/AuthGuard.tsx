'use client';

import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useSession } from "@/lib/auth-client";

export default function AuthGuard({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const { user, token, isLoading, error } = useSession();

  useEffect(() => {
    if (isLoading) return;

    // Define route groups
    const authRoutes = ['/login', '/signup'];
    // Protected routes: Tasks only (Home is public)
    const isProtectedRoute = pathname.startsWith('/tasks');
    const isAuthRoute = authRoutes.includes(pathname);

    if (user && token && !error) {
      if (isAuthRoute) {
        // If logged in and trying to access login/signup, redirect to dashboard
        router.push('/');
      }
    } else {
      // Treat error (e.g. connection failed) as not logged in
      if (isProtectedRoute) {
        // If not logged in and trying to access protected route, redirect to login
        router.push('/login');
      }
    }
  }, [pathname, router, user, token, isLoading, error]);

  const isProtectedRoute = pathname.startsWith('/tasks');

  // Show spinner ONLY if we are loading AND on a protected route.
  // This allows Navbar and Public pages to render immediately.
  if (isLoading && isProtectedRoute) {
     return (
        <div className="flex items-center justify-center min-h-screen">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
        </div>
     );
  }

  // If we are NOT loading, but unauthorized for a protected route, we render nothing (useEffect redirects)
  if (!isLoading && !user && isProtectedRoute) {
      return null; 
  }

  return <>{children}</>;
}
