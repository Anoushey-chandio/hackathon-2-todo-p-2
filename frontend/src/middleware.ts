import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Use the session token from cookies to determine auth state
  // Better Auth / our implementation uses "better-auth.session_token" or similar
  // We can also check for a custom token if we set one
  const sessionToken = request.cookies.get('better-auth.session_token')?.value || 
                       request.cookies.get('token')?.value;

  const { pathname } = request.nextUrl;

  // 1. Protect Dashboard Routes
  // If trying to access dashboard and NOT logged in -> Redirect to Login
  if (pathname.startsWith('/tasks')) {
    if (!sessionToken) {
      const url = request.nextUrl.clone();
      url.pathname = '/login';
      return NextResponse.redirect(url);
    }
  }

  // 2. Protect Auth Routes
  // If trying to access login/signup and ARE logged in -> Redirect to Dashboard
  if (pathname === '/login' || pathname === '/signup') {
    if (sessionToken) {
      const url = request.nextUrl.clone();
      url.pathname = '/';
      return NextResponse.redirect(url);
    }
  }

  return NextResponse.next();
}

// Configure which paths the middleware runs on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - assets (public assets)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|assets).*)',
  ],
};
