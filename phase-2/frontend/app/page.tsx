'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/auth';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function HomePage() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading) {
      if (isAuthenticated) {
        router.push('/dashboard');
      } else {
        router.push('/login');
      }
    }
  }, [isAuthenticated, isLoading, router]);

  // Show a loading state while checking authentication
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50 p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold">Todo App</CardTitle>
          
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-center text-gray-600">
            Welcome to the Todo application. Please sign in to continue or create an account.
          </p>
          <div className="flex flex-col space-y-2">
            <Button
              onClick={() => router.push('/login')}
              className="w-full"
            >
              Sign In
            </Button>
            <Button
              variant="outline"
              onClick={() => router.push('/signup')}
              className="w-full"
            >
              Create Account
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}