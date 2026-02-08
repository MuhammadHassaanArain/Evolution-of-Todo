/**
 * Centralized error handling for API responses
 */

interface ApiErrorHandler {
  handle401: () => void;
  handle403: () => void;
  handle4xx: (status: number, message?: string) => void;
  handle5xx: (status: number, message?: string) => void;
}

class ApiErrorHandlers implements ApiErrorHandler {
  handle401(): void {
    // Remove authentication token
    localStorage.removeItem('token');

    // Redirect to login
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  }

  handle403(): void {
    // Show access denied message or redirect to error page
    if (typeof window !== 'undefined') {
      window.location.href = '/error/access-denied';
    }
  }

  handle4xx(status: number, message?: string): void {
    // Handle client errors (4xx) - show user-friendly error
    console.error(`Client error (${status}):`, message || 'Client request error');
    // Could show a toast notification or error modal to the user
  }

  handle5xx(status: number, message?: string): void {
    // Handle server errors (5xx) - generic failure state
    console.error(`Server error (${status}):`, message || 'Server error occurred');
    // Could show a generic error message to the user
  }

  /**
   * Processes an API response and handles errors based on status code
   * @param response The fetch response
   * @returns Boolean indicating if the response was an error
   */
  async processResponse(response: Response): Promise<boolean> {
    if (response.status === 401) {
      this.handle401();
      return true;
    }

    if (response.status === 403) {
      this.handle403();
      return true;
    }

    if (response.status >= 400 && response.status < 500) {
      const data = await response.json().catch(() => ({}));
      this.handle4xx(response.status, data.error?.message);
      return true;
    }

    if (response.status >= 500) {
      const data = await response.json().catch(() => ({}));
      this.handle5xx(response.status, data.error?.message);
      return true;
    }

    return false;
  }
}

export default ApiErrorHandlers;