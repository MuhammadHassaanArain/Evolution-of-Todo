import { LoginCredentials, RegisterCredentials, AuthToken, AuthUser, AuthResponse, AuthError } from '../types/auth';
import { apiClient } from '../lib/api/client';


/**
 * Register a new user
 */
export const register = async (credentials: RegisterCredentials): Promise<AuthResponse> => {
  // Registration doesn't require auth, so we set requiresAuth to false
  const response = await apiClient.post<AuthResponse>('/auth/register', credentials, { requiresAuth: false });

  // Store the token in localStorage and cookies
  if (response.access_token) {
    localStorage.setItem('access_token', response.access_token);
    // Also set as a cookie for server-side access
    document.cookie = `access_token=${response.access_token}; path=/; max-age=3600; SameSite=Lax;`;
  }

  return response;
};

/**
 * Login a user
 */
export const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  // Login doesn't require auth, so we set requiresAuth to false
  const response = await apiClient.post<AuthResponse>('/auth/login', credentials, { requiresAuth: false });

  // Store the token in localStorage and cookies
  if (response.access_token) {
    localStorage.setItem('access_token', response.access_token);
    // Also set as a cookie for server-side access
    document.cookie = `access_token=${response.access_token}; path=/; max-age=3600; SameSite=Lax;`;
  }

  return response;
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
    await apiClient.post('/auth/logout', {}, { requiresAuth: true });
  } catch (error) {
    // Even if the server logout fails, we still clear the client-side token
    console.warn('Logout request failed, but clearing local token anyway', error);
  } finally {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token');
    // Also clear the cookie
    document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
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

  // Use the apiClient to ensure proper URL construction and headers
  const response = await apiClient.get<AuthUser>('/auth/me', { requiresAuth: true });

  return response;
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