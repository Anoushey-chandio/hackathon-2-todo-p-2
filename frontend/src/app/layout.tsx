'use client';

import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import type { Metadata } from "next";
import "../globals.css";

// Metadata is server-side only, so keep it separate or in page.tsx
// export const metadata: Metadata = {
//   title: "Todo App Phase II",
//   description: "The easiest way to manage your tasks",
// };

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const router = useRouter();
  const pathname = usePathname();
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
    const token = document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];

    const protectedRoutes = ['/', '/tasks', '/tasks/create', '/tasks/edit']; // Add more protected routes here
    const authRoutes = ['/login', '/signup'];

    if (token) {
      // If authenticated, redirect from auth routes to home
      if (authRoutes.includes(pathname)) {
        router.push('/');
      }
    } else {
      // If not authenticated, redirect from protected routes to login
      if (protectedRoutes.includes(pathname) || pathname.startsWith('/tasks/')) {
        router.push('/login');
      }
    }
  }, [pathname, router]);

  if (!isClient) {
    return null; // Render nothing on server side to avoid hydration mismatch
  }

  // Render children only after client-side useEffect has run
  // This helps prevent flickering or incorrect redirects
  const token = document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];
  const protectedRoutes = ['/', '/tasks', '/tasks/create', '/tasks/edit']; // Add more protected routes here
  const authRoutes = ['/login', '/signup'];
  
  // Conditionally render based on authentication state
  if (token && authRoutes.includes(pathname)) {
    return null; // Don't render auth pages if logged in (will be redirected by useEffect)
  }
  if (!token && (protectedRoutes.includes(pathname) || pathname.startsWith('/tasks/'))) {
    return null; // Don't render protected pages if not logged in (will be redirected by useEffect)
  }

  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
