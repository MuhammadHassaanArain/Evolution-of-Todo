/**
 * Utility functions for handling authentication-based redirects
 */

/**
 * Checks if the user should be redirected when accessing auth pages
 * @param isAuthenticated Whether the user is currently authenticated
 * @param currentPath The current route path
 * @returns boolean indicating if redirect is needed
 */
export function shouldRedirectFromAuthPages(isAuthenticated: boolean, currentPath: string): boolean {
  const authPaths = ['/login', '/signup'];
  return isAuthenticated && authPaths.some(path => currentPath.startsWith(path));
}

/**
 * Checks if the user should be redirected when accessing protected pages
 * @param isAuthenticated Whether the user is currently authenticated
 * @param currentPath The current route path
 * @returns boolean indicating if redirect is needed
 */
export function shouldRedirectToLogin(isAuthenticated: boolean, currentPath: string): boolean {
  const protectedPaths = ['/dashboard', '/profile', '/todos'];
  return !isAuthenticated && protectedPaths.some(path => currentPath.startsWith(path));
}

/**
 * Gets the redirect destination for authenticated users on auth pages
 * @returns The path to redirect authenticated users to
 */
export function getRedirectForAuthenticated(): string {
  return '/dashboard';
}

/**
 * Gets the redirect destination for unauthenticated users on protected pages
 * @param attemptedPath The path the user tried to access
 * @returns The path to redirect unauthenticated users to
 */
export function getRedirectForUnauthenticated(attemptedPath: string): string {
  return `/login?redirect=${encodeURIComponent(attemptedPath)}`;
}