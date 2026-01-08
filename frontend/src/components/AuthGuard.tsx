'use client';

import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { authClient } from "@/lib/auth-client";

export default function AuthGuard({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const { data: session, isPending } = authClient.useSession();
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    if (isPending) return;

    // Define route groups
    const authRoutes = ['/login', '/signup'];
    // Protected routes: Home and Tasks
    const isProtectedRoute = pathname === '/' || pathname.startsWith('/tasks');
    const isAuthRoute = authRoutes.includes(pathname);

    if (session) {
      if (isAuthRoute) {
        // If logged in and trying to access login/signup, redirect to dashboard
        router.push('/');
      } else {
        setAuthorized(true);
      }
    } else {
      if (isProtectedRoute) {
        // If not logged in and trying to access protected route, redirect to login
        router.push('/login');
      } else {
        // Allow access to public routes (if any) or auth routes
        setAuthorized(true);
      }
    }
  }, [pathname, router, session, isPending]);

  if (isPending || !authorized) {
     return (
        <div className="flex items-center justify-center min-h-screen">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
        </div>
     );
  }

  return <>{children}</>;
}
