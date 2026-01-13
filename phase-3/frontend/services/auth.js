import { apiClient } from './api-client';

class AuthService {
  constructor() {
    this.currentUser = null;
    this.token = null;
    this.tokenKey = 'access_token'; // Use consistent token key

    // Initialize from localStorage on construction
    this.initFromStorage();
  }

  // Initialize from localStorage
  initFromStorage() {
    const token = this.getTokenFromStorage();
    if (token) {
      this.token = token;
      apiClient.setToken(token);
    }
  }

  // Helper to get token from multiple storage locations
  getTokenFromStorage() {
    return localStorage.getItem(this.tokenKey) || localStorage.getItem('token');
  }

  // Register a new user
  async register(userData) {
    try {
      const response = await apiClient.register(userData);
      if (response && response.access_token) {
        this.setToken(response.access_token);
        this.currentUser = response.user || response;
        return response;
      }
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }

  // Login user
  async login(credentials) {
    try {
      const response = await apiClient.login(credentials);
      if (response && response.access_token) {
        this.setToken(response.access_token);
        this.currentUser = response.user || response;
        return response;
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  // Logout user
  async logout() {
    try {
      await apiClient.logout();
    } catch (error) {
      console.error('Logout error:', error);
      // Even if the API logout fails, we should still clear local state
    } finally {
      this.clearAuth();
    }
  }

  // Get current user profile
  async getProfile() {
    try {
      const response = await apiClient.getProfile();
      this.currentUser = response;
      return response;
    } catch (error) {
      console.error('Get profile error:', error);
      // If getting profile fails, clear auth state
      if (error.message.includes('Unauthorized') || error.message.includes('401')) {
        this.clearAuth();
      }
      throw error;
    }
  }

  // Set authentication token
  setToken(token) {
    this.token = token;
    apiClient.setToken(token);
    localStorage.setItem(this.tokenKey, token);
    // Also store in the other location for compatibility
    localStorage.setItem('token', token);
    // Also set as a cookie for server-side access
    if (typeof document !== 'undefined') {
      document.cookie = `access_token=${token}; path=/; max-age=3600; SameSite=Lax;`;
    }
  }

  // Get current token
  getToken() {
    return this.token;
  }

  // Clear authentication state
  clearAuth() {
    this.token = null;
    this.currentUser = null;
    apiClient.removeToken();
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem('token');
    // Also clear the cookie
    if (typeof document !== 'undefined') {
      document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
  }

  // Check if user is authenticated
  isAuthenticated() {
    const token = this.getTokenFromStorage();
    return !!token;
  }

  // Get current user
  getCurrentUser() {
    return this.currentUser;
  }

  // Check if token is expired (basic check, actual validation happens on API calls)
  isTokenExpired() {
    const token = this.getTokenFromStorage();
    if (!token) {
      return true;
    }

    try {
      // Decode the token to check expiration
      const payload = this.parseJwt(token);
      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp < currentTime;
    } catch (error) {
      console.error('Error checking token expiration:', error);
      return true;
    }
  }

  // Parse JWT token to get payload
  parseJwt(token) {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );

      return JSON.parse(jsonPayload);
    } catch (error) {
      console.error('Error parsing JWT:', error);
      throw error;
    }
  }
}

// Create a singleton instance
const authService = new AuthService();

export default authService;