import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(req: NextRequest) {
  const { pathname, searchParams } = req.nextUrl;

  // Skip static files, RSC requests, and API routes
  if (
    pathname.startsWith('/_next') ||
    pathname.startsWith('/api') ||
    searchParams.has('_rsc')
  ) {
    return NextResponse.next();
  }

  // Read session token from cookie
  const token = req.cookies.get('access_token')?.value;

  // Protect /tasks routes
  if (pathname.startsWith('/tasks') && !token) {
    const loginUrl = req.nextUrl.clone();
    loginUrl.pathname = '/signin';
    return NextResponse.redirect(loginUrl);
  }

  // Redirect logged-in users away from auth pages
  if ((pathname === '/signin' || pathname === '/signup') && token) {
    const homeUrl = req.nextUrl.clone();
    homeUrl.pathname = '/';
    return NextResponse.redirect(homeUrl);
  }

  return NextResponse.next();
}

// Apply middleware to page routes only
export const config = {
  matcher: ['/tasks/:path*', '/signin', '/signup', '/'],
};
