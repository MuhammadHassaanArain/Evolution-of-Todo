import { LoginCredentials, RegisterCredentials, AuthToken, AuthUser, AuthResponse, AuthError } from '../types/auth';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

/**
 * Register a new user
 */
export const register = async (credentials: RegisterCredentials): Promise<AuthResponse> => {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  });

  const data = await response.json();

  if (!response.ok) {
    const error: AuthError = data;
    throw new Error(error.detail || 'Registration failed');
  }

  // Store the token in localStorage
  if (data.access_token) {
    localStorage.setItem('access_token', data.access_token);
  }

  return data as AuthResponse;
};

/**
 * Login a user
 */
export const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  });

  const data = await response.json();

  if (!response.ok) {
    const error: AuthError = data;
    throw new Error(error.detail || 'Login failed');
  }

  // Store the token in localStorage
  if (data.access_token) {
    localStorage.setItem('access_token', data.access_token);
  }

  return data as AuthResponse;
};

/**
 * Logout a user
 */
export const logout = async (): Promise<void> => {
  // Remove the token from localStorage
  localStorage.removeItem('access_token');
  localStorage.removeItem('token'); // Also clear the other token key

  // In a stateless JWT system, the server doesn't store sessions
  // So we just clear the client-side token
  try {
    // Use the apiClient for consistency
    const token = localStorage.getItem('access_token');
    if (token) {
      await fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
    }
  } catch (error) {
    // Even if the server logout fails, we still clear the client-side token
    console.warn('Logout request failed, but clearing local token anyway', error);
  } finally {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token');
  }
};

/**
 * Get current user info
 */
export const getCurrentUser = async (): Promise<AuthUser> => {
  const token = localStorage.getItem('access_token');

  if (!token) {
    throw new Error('No authentication token found');
  }

  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  const data = await response.json();

  if (!response.ok) {
    const error: AuthError = data;
    throw new Error(error.detail || 'Failed to get user info');
  }

  return data as AuthUser;
};

/**
 * Get current user info (alias for getCurrentUser)
 */
export const getProfile = async (): Promise<AuthUser> => {
  return getCurrentUser();
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = (): boolean => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    return false;
  }

  // Check if token is expired
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Math.floor(Date.now() / 1000);
    return payload.exp > currentTime;
  } catch (error) {
    return false;
  }
};

/**
 * Check if token is about to expire (within 5 minutes)
 */
export const isTokenExpiringSoon = (): boolean => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    return false;
  }

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Math.floor(Date.now() / 1000);
    const fiveMinutes = 5 * 60; // 5 minutes in seconds
    return payload.exp - currentTime < fiveMinutes;
  } catch (error) {
    return true; // If we can't parse, assume it's expiring
  }
};

/**
 * Get time until token expiration in seconds
 */
export const getTimeUntilExpiration = (): number | null => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    return null;
  }

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Math.floor(Date.now() / 1000);
    return Math.max(0, payload.exp - currentTime);
  } catch (error) {
    return null;
  }
};

/**
 * Get token expiration time
 */
export const getTokenExpiration = (): number | null => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    return null;
  }

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.exp;
  } catch (error) {
    return null;
  }
};