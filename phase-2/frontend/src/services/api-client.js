// API Client Service for frontend
class ApiClient {
  constructor() {
    // Use consistent API URL with the environment config
    this.baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
    // Normalize the base URL to ensure it doesn't end with a slash
    if (this.baseURL.endsWith('/')) {
      this.baseURL = this.baseURL.slice(0, -1);
    }
    this.token = null;
  }

  // Set authentication token
  setToken(token) {
    this.token = token;
    // Also store in localStorage for persistence
    if (token) {
      localStorage.setItem('access_token', token);
    }
  }

  // Remove authentication token
  removeToken() {
    this.token = null;
    // Also remove from localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('token');
  }

  // Create headers for requests
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };

    // Use the access_token from localStorage if available, otherwise fallback to token
    const token = localStorage.getItem('access_token') || localStorage.getItem('token') || this.token;
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  // Make a request
  async request(endpoint, options = {}, requiresAuth = true) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getHeaders(),
      ...options,
    };

    // If body is provided and is an object, stringify it
    if (options.body && typeof options.body === 'object') {
      config.body = JSON.stringify(options.body);
    }

    // Add auth header only if required
    if (requiresAuth) {
      const token = localStorage.getItem('access_token') || localStorage.getItem('token') || this.token;
      if (!token && requiresAuth) {
        throw new Error('Authentication required');
      }
    } else {
      // For auth requests (like login), don't add auth headers
      config.headers = {
        'Content-Type': 'application/json',
        ...options.headers
      };
    }

    try {
      const response = await fetch(url, config);

      // Handle 401 Unauthorized
      if (response.status === 401) {
        this.removeToken();
        throw new Error('Unauthorized: Please log in again');
      }

      // Handle 403 Forbidden
      if (response.status === 403) {
        throw new Error('Forbidden: You do not have permission to access this resource');
      }

      // Try to parse response as JSON
      let data;
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        // For non-JSON responses (like DELETE), just return status
        if (response.status === 204) {
          return { success: true };
        }
        data = await response.text();
      }

      if (!response.ok) {
        throw new Error(data.detail || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  }

  // Authentication methods
  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      body: userData,
    }, false); // Don't require auth for registration
  }

  async login(credentials) {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: credentials,
    }, false); // Don't require auth for login

    // Store the token for future requests
    if (response && response.access_token) {
      this.setToken(response.access_token);
    }

    return response;
  }

  async logout() {
    // Remove the token from the client
    this.removeToken();

    // Optionally notify the backend (in JWT stateless systems, this is often client-side only)
    return this.request('/auth/logout', {
      method: 'POST',
    }, false); // Don't require auth for logout
  }

  async getProfile() {
    return this.request('/auth/me');
  }

  // Task methods
  async getTasks(offset = 0, limit = 100) {
    return this.request(`/tasks?offset=${offset}&limit=${limit}`);
  }

  async createTask(taskData) {
    return this.request('/tasks', {
      method: 'POST',
      body: taskData,
    });
  }

  async getTask(taskId) {
    return this.request(`/tasks/${taskId}`);
  }

  async updateTask(taskId, taskData) {
    return this.request(`/tasks/${taskId}`, {
      method: 'PUT',
      body: taskData,
    });
  }

  async deleteTask(taskId) {
    return this.request(`/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }
}

// Create a singleton instance
const apiClient = new ApiClient();

export default apiClient;