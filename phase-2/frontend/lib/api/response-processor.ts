/**
 * Processes API responses to normalize data and handle common patterns
 */

interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
}

class ApiResponseProcessor {
  /**
   * Processes a successful API response
   * @param response The fetch response
   * @returns Normalized response data
   */
  async processSuccess<T>(response: Response): Promise<ApiResponse<T>> {
    if (response.status === 204) {
      // No content response
      return {
        success: true,
        data: undefined as T,
        message: 'Success'
      };
    }

    const data = await response.json();

    return {
      success: true,
      data: data.data || data,
      message: data.message || 'Success'
    };
  }

  /**
   * Processes an error API response
   * @param response The fetch response
   * @returns Normalized error response
   */
  async processError(response: Response): Promise<ApiResponse> {
    let errorData;
    try {
      errorData = await response.json();
    } catch (e) {
      // If response is not JSON, create a generic error
      errorData = {
        error: {
          code: `HTTP_${response.status}`,
          message: response.statusText || 'An error occurred'
        }
      };
    }

    return {
      success: false,
      error: errorData.error || {
        code: `HTTP_${response.status}`,
        message: errorData.message || response.statusText || 'An error occurred'
      }
    };
  }

  /**
   * Processes a response based on its status
   * @param response The fetch response
   * @returns Normalized response
   */
  async process<T>(response: Response): Promise<ApiResponse<T>> {
    if (response.ok) {
      return this.processSuccess<T>(response);
    } else {
      return this.processError(response);
    }
  }

  /**
   * Normalizes different response formats to a consistent structure
   * @param data The raw response data
   * @returns Normalized data structure
   */
  normalizeData<T>(data: any): T {
    // If data is already in our expected format, return as-is
    if (data && typeof data === 'object' && 'success' in data) {
      return data as T;
    }

    // If data is a simple object/array, wrap it in our structure
    return {
      success: true,
      data: data,
      message: 'Success'
    } as T;
  }
}

export default ApiResponseProcessor;