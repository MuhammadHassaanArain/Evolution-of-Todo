/**
 * Authentication interceptor for API requests
 * Handles adding authentication tokens to requests and processing auth-related responses
 */

interface InterceptorConfig {
  getToken: () => string | null;
  onAuthError: (error: Error) => void;
  onTokenExpired: () => void;
}

class AuthInterceptor {
  private config: InterceptorConfig;

  constructor(config: InterceptorConfig) {
    this.config = config;
  }

  /**
   * Intercepts a request and adds authentication headers
   * @param request The request configuration
   * @returns Modified request with auth headers
   */
  interceptRequest(request: RequestInit & { url?: string }): RequestInit & { url?: string } {
    const token = this.config.getToken();

    if (token) {
      request.headers = {
        ...request.headers,
        'Authorization': `Bearer ${token}`
      };
    }

    return request;
  }

  /**
   * Intercepts a response and handles auth-related status codes
   * @param response The fetch response
   * @returns The processed response
   */
  async interceptResponse(response: Response): Promise<Response> {
    // Handle 401 Unauthorized responses
    if (response.status === 401) {
      this.config.onTokenExpired();
      throw new Error('Authentication token has expired');
    }

    // Handle 403 Forbidden responses
    if (response.status === 403) {
      this.config.onAuthError(new Error('Access forbidden'));
    }

    return response;
  }

  /**
   * Adds authentication headers to a request configuration
   * @param headers Existing headers to extend
   * @returns Headers with authentication token added
   */
  addAuthHeader(headers: Record<string, string> = {}): Record<string, string> {
    const token = this.config.getToken();

    if (token) {
      return {
        ...headers,
        'Authorization': `Bearer ${token}`
      };
    }

    return headers;
  }

  /**
   * Checks if a response indicates an authentication error
   * @param response The fetch response
   * @returns Boolean indicating if auth error occurred
   */
  isAuthError(response: Response): boolean {
    return response.status === 401 || response.status === 403;
  }
}

export default AuthInterceptor;