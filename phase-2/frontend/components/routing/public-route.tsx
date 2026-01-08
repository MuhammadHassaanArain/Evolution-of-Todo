import { useAuth } from '@/contexts/auth';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

interface PublicRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  redirectTo?: string; // Where to redirect authenticated users (default: '/dashboard')
}

export default function PublicRoute({
  children,
  fallback = <div>Redirecting...</div>,
  redirectTo = '/dashboard'
}: PublicRouteProps) {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    // If we know the auth status, handle routing
    if (isAuthenticated !== null) {
      setIsChecking(false);

      // If authenticated, redirect to the specified route
      if (isAuthenticated) {
        router.push(redirectTo);
      }
    }
  }, [isAuthenticated, router, redirectTo]);

  // Show fallback while checking auth status or if authenticated
  if (isChecking || isAuthenticated) {
    return fallback;
  }

  // If not authenticated, render children
  return <>{children}</>;
}