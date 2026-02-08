import { NextRequest, NextResponse } from 'next/server'

/**
 * Checks if a route requires authentication
 * @param pathname The route path to check
 * @returns boolean indicating if the route is protected
 */
export function isProtectedRoute(pathname: string): boolean {
  const protectedPaths = ['/dashboard', '/profile', '/todos'];
  return protectedPaths.some(path => pathname.startsWith(path));
}

/**
 * Checks if a route is an authentication route
 * @param pathname The route path to check
 * @returns boolean indicating if the route is an auth route
 */
export function isAuthRoute(pathname: string): boolean {
  const authPaths = ['/login', '/signup'];
  return authPaths.some(path => pathname.startsWith(path));
}

/**
 * Gets the redirect path for unauthenticated access to protected routes
 * @param currentPath The current path that requires authentication
 * @returns The path to redirect to
 */
export function getLoginRedirectPath(currentPath: string): string {
  return `/login?redirect=${encodeURIComponent(currentPath)}`;
}

/**
 * Gets the redirect path for authenticated users on auth pages
 * @returns The path to redirect authenticated users to
 */
export function getAuthRedirectPath(): string {
  return '/dashboard';
}