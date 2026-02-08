import { getRedirectForUnauthenticated } from '../auth/auth-redirects';

interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  headers?: Record<string, string>;
  body?: any;
  requiresAuth?: boolean;
}

class ApiClient {
  private baseUrl: string;
  private defaultHeaders: Record<string, string>;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    // Normalize the base URL to ensure it doesn't end with a slash
    if (this.baseUrl.endsWith('/')) {
      this.baseUrl = this.baseUrl.slice(0, -1);
    }
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  private async request<T>(endpoint: string, options: ApiOptions = {}): Promise<T> {
    const {
      method = 'GET',
      headers = {},
      body,
      requiresAuth = true,
    } = options;

    let requestHeaders = { ...this.defaultHeaders, ...headers };

    // Add authorization header if required
    if (requiresAuth) {
      const token = this.getToken();
      if (token) {
        requestHeaders['Authorization'] = `Bearer ${token}`;
      } else if (requiresAuth) {
        // Redirect to login if auth is required but no token exists
        if (typeof window !== 'undefined') {
          window.location.href = getRedirectForUnauthenticated(window.location.pathname);
        }
        throw new Error('Authentication required');
      }
    }

    // Ensure the endpoint starts with /api if it's not already part of the endpoint
    let normalizedEndpoint = endpoint;
    if (!normalizedEndpoint.startsWith('/api/')) {
      if (normalizedEndpoint.startsWith('/')) {
        normalizedEndpoint = `/api${normalizedEndpoint}`;
      } else {
        normalizedEndpoint = `/api/${normalizedEndpoint}`;
      }
    }

    const url = `${this.baseUrl}${normalizedEndpoint}`;

    const config: RequestInit = {
      method,
      headers: requestHeaders,
      ...(body && { body: typeof body === 'string' ? body : JSON.stringify(body) }),
    };

    try {
      const response = await fetch(url, config);

      // Handle 401 Unauthorized
      if (response.status === 401) {
        this.clearToken();
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        throw new Error('Unauthorized: Please log in again');
      }

      // Handle 403 Forbidden
      if (response.status === 403) {
        throw new Error('Access forbidden: You do not have permission to access this resource');
      }

      // Handle 422 Unprocessable Entity (validation errors)
      if (response.status === 422) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Validation error occurred');
      }

      // Handle 5xx Server errors
      if (response.status >= 500) {
        throw new Error(`Server error: ${response.status} - ${response.statusText}`);
      }

      // For 204 No Content responses, return null
      if (response.status === 204) {
        return null as T;
      }

      // Try to parse response as JSON, fallback to text if not JSON
      let data;
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        data = await response.text();
      }

      if (!response.ok) {
        // Handle different error status codes
        if (response.status >= 400 && response.status < 500) {
          const errorMessage = typeof data === 'object' && data.detail
            ? data.detail
            : `Client error: ${response.status} - ${response.statusText}`;
          throw new Error(errorMessage);
        } else {
          throw new Error(`Request failed with status ${response.status}`);
        }
      }

      return data;
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  }

  // Helper method to get token from multiple possible storage locations
  private getToken(): string | null {
    return localStorage.getItem('access_token') || localStorage.getItem('token');
  }

  // Helper method to clear all token storage locations
  private clearToken(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token');
  }

  get<T>(endpoint: string, options: Omit<ApiOptions, 'method'> = {}): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' });
  }

  post<T>(endpoint: string, body: any, options: Omit<ApiOptions, 'method'> = {}): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'POST', body });
  }

  put<T>(endpoint: string, body: any, options: Omit<ApiOptions, 'method'> = {}): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'PUT', body });
  }

  delete<T>(endpoint: string, options: Omit<ApiOptions, 'method'> = {}): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();