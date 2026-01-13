import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from '@/contexts/auth';
import userEvent from '@testing-library/user-event';

// Mock the next/navigation module
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
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

// Mock fetch
global.fetch = jest.fn();

// Test component to access auth context
const TestComponent = () => {
  const { isAuthenticated, user, login, logout, register } = useAuth();

  return (
    <div>
      <div data-testid="isAuthenticated">{isAuthenticated ? 'true' : 'false'}</div>
      <div data-testid="user">{user ? JSON.stringify(user) : 'null'}</div>
      <button onClick={() => login('test@example.com', 'password')} data-testid="login">
        Login
      </button>
      <button onClick={logout} data-testid="logout">
        Logout
      </button>
      <button
        onClick={() =>
          register({
            email: 'new@example.com',
            password: 'password',
            username: 'newuser',
            first_name: 'New',
            last_name: 'User',
          })
        }
        data-testid="register"
      >
        Register
      </button>
    </div>
  );
};

describe('Auth Context', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (window.localStorage.getItem as jest.Mock).mockReturnValue(null);
    (global.fetch as jest.MockedFunction<typeof global.fetch>).mockClear();
  });

  it('should provide initial auth state', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByTestId('isAuthenticated')).toHaveTextContent('false');
    expect(screen.getByTestId('user')).toHaveTextContent('null');
  });

  it('should handle login', async () => {
    const mockToken = 'mock-jwt-token';
    const mockUserData = { id: 1, email: 'test@example.com', username: 'testuser' };

    (global.fetch as jest.MockedFunction<typeof global.fetch>).mockResolvedValue({
      ok: true,
      json: async () => ({
        data: { access_token: mockToken },
      }),
    } as Response);

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    const loginButton = screen.getByTestId('login');
    userEvent.click(loginButton);

    await waitFor(() => {
      expect(window.localStorage.setItem).toHaveBeenCalledWith('token', mockToken);
      expect(screen.getByTestId('isAuthenticated')).toHaveTextContent('true');
    });
  });

  it('should handle logout', async () => {
    // Set up initial authenticated state
    (window.localStorage.getItem as jest.Mock).mockReturnValue('mock-jwt-token');

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    // Wait for the component to initialize with the token
    await waitFor(() => {
      expect(screen.getByTestId('isAuthenticated')).toHaveTextContent('true');
    });

    const logoutButton = screen.getByTestId('logout');
    userEvent.click(logoutButton);

    await waitFor(() => {
      expect(window.localStorage.removeItem).toHaveBeenCalledWith('token');
      expect(screen.getByTestId('isAuthenticated')).toHaveTextContent('false');
      expect(screen.getByTestId('user')).toHaveTextContent('null');
    });
  });

  it('should handle registration', async () => {
    const mockToken = 'mock-jwt-token';

    (global.fetch as jest.MockedFunction<typeof global.fetch>).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        data: { id: 2, email: 'new@example.com', username: 'newuser' },
      }),
    } as Response);

    // Mock login after registration
    (global.fetch as jest.MockedFunction<typeof global.fetch>).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        data: { access_token: mockToken },
      }),
    } as Response);

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    const registerButton = screen.getByTestId('register');
    userEvent.click(registerButton);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledTimes(2); // Registration and then login
      expect(window.localStorage.setItem).toHaveBeenCalledWith('token', mockToken);
    });
  });
});