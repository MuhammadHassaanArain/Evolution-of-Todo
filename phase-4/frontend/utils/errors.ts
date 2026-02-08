/**
 * Centralized error handling utilities
 */

interface ErrorContext {
  component?: string;
  action?: string;
  userId?: string;
  timestamp?: string;
  errorType?: string;
  [key: string]: any; // Allow additional properties
}

class ErrorHandler {
  /**
   * Logs an error with context
   * @param error The error to log
   * @param context Additional context about where the error occurred
   */
  static logError(error: Error, context?: ErrorContext): void {
    const errorWithContext = {
      message: error.message,
      stack: error.stack,
      context: {
        timestamp: new Date().toISOString(),
        ...context,
      },
    };

    console.error('Error occurred:', errorWithContext);

    // In a real application, you might send this to an error tracking service
    // Example: Sentry.captureException(error, { contexts: { custom: context } });
  }

  /**
   * Handles API errors consistently
   * @param error The error to handle
   * @param context Additional context about the error
   */
  static handleApiError(error: any, context?: ErrorContext): void {
    let errorMessage = 'An unexpected error occurred';

    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;

      switch (status) {
        case 400:
          errorMessage = data?.message || 'Bad request';
          break;
        case 401:
          errorMessage = 'Authentication required';
          // In a real app, you might redirect to login here
          break;
        case 403:
          errorMessage = 'Access forbidden';
          break;
        case 404:
          errorMessage = 'Resource not found';
          break;
        case 500:
          errorMessage = 'Server error occurred';
          break;
        default:
          errorMessage = data?.message || `Server error (${status})`;
      }
    } else if (error.request) {
      // Request was made but no response received
      errorMessage = 'Network error - please check your connection';
    } else {
      // Something else happened
      errorMessage = error.message || errorMessage;
    }

    const apiError = new Error(errorMessage);
    this.logError(apiError, { ...context, errorType: 'API_ERROR' });

    // Re-throw with user-friendly message
    throw new Error(errorMessage);
  }

  /**
   * Creates a user-friendly error message
   * @param error The error to convert
   * @returns A user-friendly error message
   */
  static getUserFriendlyMessage(error: any): string {
    if (error.response) {
      const { status } = error.response;

      switch (status) {
        case 401:
          return 'Your session has expired. Please log in again.';
        case 403:
          return 'You do not have permission to perform this action.';
        case 404:
          return 'The requested resource could not be found.';
        case 500:
          return 'A server error occurred. Please try again later.';
        default:
          return error.response.data?.message || 'An error occurred. Please try again.';
      }
    }

    return error.message || 'An unexpected error occurred';
  }

  /**
   * Reports an error to an external service (e.g., Sentry, Bugsnag)
   * @param error The error to report
   * @param context Additional context for the error report
   */
  static reportError(error: Error, context?: ErrorContext): void {
    // In a real application, you would send this to an error tracking service
    console.log('Reporting error to external service:', { error, context });
  }
}

export default ErrorHandler;