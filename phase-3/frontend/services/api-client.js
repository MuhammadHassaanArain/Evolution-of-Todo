// API Client Service for frontend
// This file is being deprecated in favor of the TypeScript client in lib/api/client.ts
// But we'll keep it for backward compatibility
import { apiClient as tsApiClient } from '../lib/api/client';

// Create a wrapper to maintain compatibility with existing code
class ApiClientWrapper {
  constructor() {
    // Use the TypeScript API client as the base
    this.tsClient = tsApiClient;
  }

  // Set authentication token
  setToken(token) {
    // The TypeScript client handles token storage in localStorage automatically
    // We just need to ensure it's stored in localStorage for other parts of the app
    if (token) {
      localStorage.setItem('access_token', token);
      localStorage.setItem('token', token);
      // Also set as a cookie for server-side access
      if (typeof document !== 'undefined') {
        document.cookie = `access_token=${token}; path=/; max-age=3600; SameSite=Lax;`;
      }
    }
  }

  // Remove authentication token
  removeToken() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token');
    // Also clear the cookie
    if (typeof document !== 'undefined') {
      document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
  }

  // Make a request - this should map to the TypeScript client methods
  async request(endpoint, options = {}, requiresAuth = true) {
    const method = options.method || 'GET';
    const body = options.body;

    try {
      switch (method) {
        case 'GET':
          return await this.tsClient.get(endpoint, { requiresAuth });
        case 'POST':
          return await this.tsClient.post(endpoint, body, { requiresAuth });
        case 'PUT':
          return await this.tsClient.put(endpoint, body, { requiresAuth });
        case 'DELETE':
          return await this.tsClient.delete(endpoint, { requiresAuth });
        default:
          throw new Error(`Unsupported method: ${method}`);
      }
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  }

  // Authentication methods
  async register(userData) {
    // Use the TypeScript client directly for auth methods
    // We'll make the call without auth requirement
    try {
      const response = await fetch(`${this.tsClient.baseUrl}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || `HTTP error! status: ${response.status}`);
      }

      // Store the token for future requests
      if (data && data.access_token) {
        this.setToken(data.access_token);
      }

      return data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }

  async login(credentials) {
    // Use direct fetch for login to avoid auth requirement
    try {
      const response = await fetch(`${this.tsClient.baseUrl}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || `HTTP error! status: ${response.status}`);
      }

      // Store the token for future requests
      if (data && data.access_token) {
        this.setToken(data.access_token);
      }

      return data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  async logout() {
    // Use direct fetch for logout to avoid auth requirement issues
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        await fetch(`${this.tsClient.baseUrl}/api/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
      }
    } catch (error) {
      console.error('Logout request failed:', error);
      // Continue with clearing the token even if the server request fails
    } finally {
      this.removeToken();
    }
  }

  async getProfile() {
    // Use the TypeScript client's get method
    return await this.tsClient.get('/auth/me');
  }

  // Task methods - use the TypeScript client
  async getTasks(offset = 0, limit = 100) {
    return await this.tsClient.get(`/tasks?offset=${offset}&limit=${limit}`, { requiresAuth: false });
  }

  async createTask(taskData) {
    return await this.tsClient.post('/tasks', taskData, { requiresAuth: false });
  }

  async getTask(taskId) {
    return await this.tsClient.get(`/tasks/${taskId}`, { requiresAuth: false });
  }

  async updateTask(taskId, taskData) {
    return await this.tsClient.put(`/tasks/${taskId}`, taskData, { requiresAuth: false });
  }

  async deleteTask(taskId) {
    return await this.tsClient.delete(`/tasks/${taskId}`, { requiresAuth: false });
  }
}

// Create a singleton instance
const apiClient = new ApiClientWrapper();

export default apiClient;