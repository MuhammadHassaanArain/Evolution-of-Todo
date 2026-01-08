import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

interface UseAuthGuardOptions {
  redirectTo?: string;
  redirectIfAuthenticated?: string;
}

/**
 * Custom hook for handling authentication checks and redirects
 * @param options Configuration options for the auth guard
 * @returns Object containing auth status and redirect function
 */
export function useAuthGuard(options: UseAuthGuardOptions = {}) {
  const { redirectTo = '/login', redirectIfAuthenticated = '/dashboard' } = options;
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null); // null means loading
  const [loading, setLoading] = useState<boolean>(true);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = () => {
      try {
        const token = localStorage.getItem('token');
        const isValid = validateToken(token);
        setIsAuthenticated(isValid);
      } catch (error) {
        console.error('Auth validation error:', error);
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  useEffect(() => {
    if (isAuthenticated === false && !loading) {
      // Redirect to login if not authenticated
      const redirectUrl = `${redirectTo}?redirect=${encodeURIComponent(window.location.pathname)}`;
      router.push(redirectUrl);
    } else if (isAuthenticated === true && !loading) {
      // If user is authenticated but on an auth page, redirect to dashboard
      const authPages = ['/login', '/signup'];
      if (authPages.some(page => window.location.pathname.startsWith(page)) && redirectIfAuthenticated) {
        router.push(redirectIfAuthenticated);
      }
    }
  }, [isAuthenticated, loading, redirectTo, redirectIfAuthenticated, router]);

  /**
   * Validates the JWT token
   * @param token The JWT token to validate
   * @returns Boolean indicating if the token is valid
   */
  const validateToken = (token: string | null): boolean => {
    if (!token) {
      return false;
    }

    try {
      // Decode the token to check if it's valid
      const tokenParts = token.split('.');
      if (tokenParts.length !== 3) {
        return false;
      }

      // Decode the payload part (second part)
      const payload = JSON.parse(atob(tokenParts[1]));

      // Check if the token has expired
      const currentTime = Math.floor(Date.now() / 1000);
      if (payload.exp && payload.exp < currentTime) {
        // Token has expired
        localStorage.removeItem('token');
        return false;
      }

      return true;
    } catch (error) {
      console.error('Token validation error:', error);
      return false;
    }
  };

  /**
   * Manually checks authentication status
   * @returns Boolean indicating if user is authenticated
   */
  const checkAuth = (): boolean => {
    const token = localStorage.getItem('token');
    return validateToken(token);
  };

  /**
   * Redirects to login page with optional redirect path
   * @param redirectPath Path to redirect to after login
   */
  const redirectToLogin = (redirectPath?: string) => {
    const redirectParam = redirectPath ? `?redirect=${encodeURIComponent(redirectPath)}` : '';
    router.push(`${redirectTo}${redirectParam}`);
  };

  return {
    isAuthenticated: isAuthenticated,
    loading,
    checkAuth,
    redirectToLogin,
  };
}