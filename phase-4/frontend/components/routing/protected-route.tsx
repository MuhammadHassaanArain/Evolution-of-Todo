import { useAuth } from '@/contexts/auth';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export default function ProtectedRoute({ children, fallback = <div>Redirecting...</div> }: ProtectedRouteProps) {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    // If we know the auth status, handle routing
    if (isAuthenticated !== null) {
      setIsChecking(false);

      // If not authenticated, redirect to login
      if (!isAuthenticated) {
        const redirectPath = `/login?redirect=${encodeURIComponent(window.location.pathname)}`;
        router.push(redirectPath);
      }
    }
  }, [isAuthenticated, router]);

  // Show fallback while checking auth status or if not authenticated
  if (isChecking || !isAuthenticated) {
    return fallback;
  }

  // If authenticated, render children
  return <>{children}</>;
}