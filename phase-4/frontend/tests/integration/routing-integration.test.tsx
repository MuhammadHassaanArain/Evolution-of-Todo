import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { AuthProvider } from '@/contexts/auth';
import ProtectedRoute from '@/components/routing/protected-route';
import PublicRoute from '@/components/routing/public-route';
import { useRouter } from 'next/navigation';

// Mock the next/navigation module
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
  useSearchParams: () => ({
    get: jest.fn(),
  }),
}));

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('Routing Integration', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('ProtectedRoute', () => {
    it('should render children when authenticated', async () => {
      (window.localStorage.getItem as jest.Mock).mockReturnValue('mock-jwt-token');
      (useRouter as jest.Mock).mockReturnValue({
        push: jest.fn(),
      });

      render(
        <AuthProvider>
          <ProtectedRoute>
            <div data-testid="protected-content">Protected Content</div>
          </ProtectedRoute>
        </AuthProvider>
      );

      await waitFor(() => {
        expect(screen.getByTestId('protected-content')).toBeInTheDocument();
      });
    });

    it('should show fallback when not authenticated', async () => {
      (window.localStorage.getItem as jest.Mock).mockReturnValue(null);
      const mockPush = jest.fn();
      (useRouter as jest.Mock).mockReturnValue({
        push: mockPush,
      });

      render(
        <AuthProvider>
          <ProtectedRoute fallback={<div data-testid="redirecting">Redirecting...</div>}>
            <div data-testid="protected-content">Protected Content</div>
          </ProtectedRoute>
        </AuthProvider>
      );

      await waitFor(() => {
        expect(screen.getByTestId('redirecting')).toBeInTheDocument();
        expect(mockPush).toHaveBeenCalledWith('/login?redirect=' + encodeURIComponent(window.location.pathname));
      });
    });
  });

  describe('PublicRoute', () => {
    it('should render children when not authenticated', async () => {
      (window.localStorage.getItem as jest.Mock).mockReturnValue(null);
      (useRouter as jest.Mock).mockReturnValue({
        push: jest.fn(),
      });

      render(
        <AuthProvider>
          <PublicRoute>
            <div data-testid="public-content">Public Content</div>
          </PublicRoute>
        </AuthProvider>
      );

      await waitFor(() => {
        expect(screen.getByTestId('public-content')).toBeInTheDocument();
      });
    });

    it('should redirect when authenticated', async () => {
      (window.localStorage.getItem as jest.Mock).mockReturnValue('mock-jwt-token');
      const mockPush = jest.fn();
      (useRouter as jest.Mock).mockReturnValue({
        push: mockPush,
      });

      render(
        <AuthProvider>
          <PublicRoute redirectTo="/dashboard">
            <div data-testid="public-content">Public Content</div>
          </PublicRoute>
        </AuthProvider>
      );

      await waitFor(() => {
        expect(mockPush).toHaveBeenCalledWith('/dashboard');
      });
    });
  });

  describe('Auth Redirects', () => {
    it('should redirect authenticated users from login page', async () => {
      // Mock that we're on the login page
      Object.defineProperty(window, 'location', {
        value: {
          pathname: '/login',
        },
        writable: true,
      });

      (window.localStorage.getItem as jest.Mock).mockReturnValue('mock-jwt-token');
      const mockPush = jest.fn();
      (useRouter as jest.Mock).mockReturnValue({
        push: mockPush,
      });

      render(
        <AuthProvider>
          <PublicRoute redirectTo="/dashboard">
            <div data-testid="login-form">Login Form</div>
          </PublicRoute>
        </AuthProvider>
      );

      await waitFor(() => {
        expect(mockPush).toHaveBeenCalledWith('/dashboard');
      });
    });

    it('should redirect unauthenticated users from dashboard', async () => {
      // Mock that we're on the dashboard page
      Object.defineProperty(window, 'location', {
        value: {
          pathname: '/dashboard',
        },
        writable: true,
      });

      (window.localStorage.getItem as jest.Mock).mockReturnValue(null);
      const mockPush = jest.fn();
      (useRouter as jest.Mock).mockReturnValue({
        push: mockPush,
      });

      render(
        <AuthProvider>
          <ProtectedRoute>
            <div data-testid="dashboard">Dashboard</div>
          </ProtectedRoute>
        </AuthProvider>
      );

      await waitFor(() => {
        expect(mockPush).toHaveBeenCalledWith('/login?redirect=' + encodeURIComponent('/dashboard'));
      });
    });
  });
});