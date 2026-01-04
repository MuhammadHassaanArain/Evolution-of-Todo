import { NextRequest, NextResponse } from 'next/server'

export function middleware(req: NextRequest) {
  // Get the token from cookies or headers
  const token = req.cookies.get('token') || req.headers.get('authorization')?.split(' ')[1]

  // Define protected routes
  const protectedPaths = ['/dashboard', '/profile', '/todos']
  const isProtectedRoute = protectedPaths.some(path => req.nextUrl.pathname.startsWith(path))

  // If the route is protected and no token exists, redirect to login
  if (isProtectedRoute && !token) {
    return NextResponse.redirect(new URL('/login', req.url))
  }

  // If user is trying to access auth pages (login/signup/forgot-password) while authenticated, redirect to dashboard
  const authPaths = ['/login', '/signup', '/forgot-password']
  const isAuthRoute = authPaths.some(path => req.nextUrl.pathname.startsWith(path))

  if (isAuthRoute && token) {
    return NextResponse.redirect(new URL('/dashboard', req.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*', '/todos/:path*', '/login', '/signup', '/forgot-password', '/']
}