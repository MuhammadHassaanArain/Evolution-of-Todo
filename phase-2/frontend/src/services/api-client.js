// API Client Service for frontend
class ApiClient {
  constructor() {
    this.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
    this.token = null;
  }

  // Set authentication token
  setToken(token) {
    this.token = token;
  }

  // Remove authentication token
  removeToken() {
    this.token = null;
  }

  // Create headers for requests
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  // Make a request
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getHeaders(),
      ...options,
    };

    // If body is provided and is an object, stringify it
    if (options.body && typeof options.body === 'object') {
      config.body = JSON.stringify(options.body);
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
    });
  }

  async login(credentials) {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: credentials,
    });

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
    });
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