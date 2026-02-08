import { NextRequest, NextResponse } from 'next/server'

export function middleware(req: NextRequest) {
  // Only check authentication for API routes
  // For page routes, authentication will be handled client-side by the AuthProvider
  if (req.nextUrl.pathname.startsWith('/api/')) {
    // Get the token from cookies or authorization header
    const token = req.cookies.get('access_token')?.value || req.cookies.get('token')?.value || req.headers.get('authorization')?.split(' ')[1]

    // Define protected API routes
    const protectedPaths = ['/api/auth/me']
    const isProtectedRoute = protectedPaths.some(path => req.nextUrl.pathname.startsWith(path))

    // If the API route is protected and no token exists, return 401
    if (isProtectedRoute && !token) {
      return NextResponse.json({ error: 'Authentication required' }, { status: 401 })
    }
  }

  // For page routes, we let them pass through and handle auth client-side
  // The client-side AuthProvider will handle redirecting unauthenticated users
  return NextResponse.next()
}

// Only run middleware on API routes
export const config = {
  matcher: [
    '/api/:path*'
  ]
}