import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '../lib/api/client';

interface UseApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  requiresAuth?: boolean;
  autoTrigger?: boolean;
}

interface UseApiReturn<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

function useApi<T>(
  endpoint: string,
  options: UseApiOptions = {}
): UseApiReturn<T> {
  const { method = 'GET', requiresAuth = true, autoTrigger = true } = options;
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [trigger, setTrigger] = useState(0); // For manual refetching

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      let result: T;

      switch (method) {
        case 'GET':
          result = await apiClient.get<T>(endpoint, { requiresAuth });
          break;
        case 'POST':
          result = await apiClient.post<T>(endpoint, null, { requiresAuth });
          break;
        case 'PUT':
          result = await apiClient.put<T>(endpoint, null, { requiresAuth });
          break;
        case 'DELETE':
          result = await apiClient.delete<T>(endpoint, { requiresAuth });
          break;
        default:
          throw new Error(`Unsupported method: ${method}`);
      }

      setData(result);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMessage);
      console.error('API error:', err);
    } finally {
      setLoading(false);
    }
  }, [endpoint, method, requiresAuth]);

  useEffect(() => {
    if (autoTrigger) {
      fetchData();
    }
  }, [fetchData, autoTrigger, trigger]);

  const refetch = useCallback(() => {
    setTrigger(prev => prev + 1);
  }, []);

  return { data, loading, error, refetch };
}

export default useApi;