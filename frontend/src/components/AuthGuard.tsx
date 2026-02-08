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

  useEffect(() => {
    // 1. Loading ke waqt kuch nahi karna
    if (isLoading) return;

    // 2. Agar user login NAHI hai aur Protected Route (/tasks) par jane ki koshish kare
    // Toh usay signin par bhejo
    if (!user && isProtectedRoute) {
      router.replace('/signin');
      return;
    }

    // NOTE: Humne yahan se wo block hata diya hai jo logged-in user ko 
    // signin/signup se utha kar tasks par phenk deta tha.
    // Ab user login hone ke baad bhi baqi pages dekh sakega.

  }, [user, isLoading, pathname, router]);

  // ⏳ Loader sirf tab dikhayen jab user kisi protected page (/tasks) par ho aur session load ho raha ho
  if (isLoading && isProtectedRoute) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  // 🚫 Agar loading khatam ho jaye aur user login na ho, toh protected content hide rakhen
  if (!isLoading && !user && isProtectedRoute) {
    return null;
  }

  return <>{children}</>;
}