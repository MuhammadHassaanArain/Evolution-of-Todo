import { apiClient } from '@/lib/api/client';

// Mock the global fetch function
global.fetch = jest.fn();

describe('ApiClient', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();

    // Mock localStorage
    const localStorageMock = {
      getItem: jest.fn(),
      setItem: jest.fn(),
      removeItem: jest.fn(),
      clear: jest.fn(),
    };
    Object.defineProperty(window, 'localStorage', {
      value: localStorageMock,
    });
  });

  describe('GET requests', () => {
    it('should make a GET request with proper headers', async () => {
      const mockResponse = { success: true, data: { id: 1, name: 'Test' } };
      (global.fetch as jest.MockedFunction<typeof global.fetch>).mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
        status: 200,
      } as Response);

      const result = await apiClient.get('/test');

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/test',
        expect.objectContaining({
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        })
      );
      expect(result).toEqual(mockResponse);
    });

    it('should include authorization header when token is present', async () => {
      // Mock token in localStorage
      const mockToken = 'mock-jwt-token';
      (window.localStorage.getItem as jest.Mock).mockReturnValue(mockToken);

      const mockResponse = { success: true, data: { id: 1, name: 'Test' } };
      (global.fetch as jest.MockedFunction<typeof global.fetch>).mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
        status: 200,
      } as Response);

      await apiClient.get('/test', { requiresAuth: true });

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/test',
        expect.objectContaining({
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${mockToken}`,
          },
        })
      );
    });
  });

  describe('POST requests', () => {
    it('should make a POST request with body data', async () => {
      const postData = { name: 'New Item' };
      const mockResponse = { success: true, data: { id: 2, name: 'New Item' } };

      (global.fetch as jest.MockedFunction<typeof global.fetch>).mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
        status: 201,
      } as Response);

      const result = await apiClient.post('/test', postData);

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/test',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(postData),
          headers: {
            'Content-Type': 'application/json',
          },
        })
      );
      expect(result).toEqual(mockResponse);
    });
  });

  describe('Error handling', () => {
    it('should handle 401 errors by removing token and redirecting', async () => {
      (global.fetch as jest.MockedFunction<typeof global.fetch>).mockResolvedValue({
        ok: false,
        json: async () => ({ error: { message: 'Unauthorized' } }),
        status: 401,
      } as Response);

      // Mock window.location for redirect
      delete (window as any).location;
      (window as any).location = { href: '' };

      await expect(apiClient.get('/test', { requiresAuth: true })).rejects.toThrow('Unauthorized: Please log in again');

      expect(window.localStorage.removeItem).toHaveBeenCalledWith('token');
    });

    it('should handle 403 errors appropriately', async () => {
      (global.fetch as jest.MockedFunction<typeof global.fetch>).mockResolvedValue({
        ok: false,
        json: async () => ({ error: { message: 'Forbidden' } }),
        status: 403,
      } as Response);

      await expect(apiClient.get('/test')).rejects.toThrow('Access forbidden: You do not have permission to access this resource');
    });

    it('should handle 5xx errors appropriately', async () => {
      (global.fetch as jest.MockedFunction<typeof global.fetch>).mockResolvedValue({
        ok: false,
        json: async () => ({ error: { message: 'Internal Server Error' } }),
        status: 500,
      } as Response);

      await expect(apiClient.get('/test')).rejects.toThrow('Server error: 500 - Internal Server Error');
    });
  });
});