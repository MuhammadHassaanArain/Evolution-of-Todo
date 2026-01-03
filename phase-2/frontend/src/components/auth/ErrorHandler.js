import React, { useEffect } from 'react';
import { useRouter } from 'next/router';
import authService from '../../services/auth';

const ErrorHandler = ({ error, onAuthError = null }) => {
  const router = useRouter();

  useEffect(() => {
    if (error && (error.includes('Unauthorized') || error.includes('401'))) {
      // Handle unauthorized access
      authService.clearAuth();
      if (onAuthError) {
        onAuthError('unauthorized');
      } else {
        router.push('/login');
      }
    } else if (error && error.includes('Forbidden')) {
      // Handle forbidden access (403)
      if (onAuthError) {
        onAuthError('forbidden');
      }
    }
  }, [error, router, onAuthError]);

  if (!error) {
    return null;
  }

  // Determine error type and message
  let message = error;
  let type = 'error';

  if (error.includes('Unauthorized')) {
    message = 'Your session has expired. Please log in again.';
    type = 'warning';
  } else if (error.includes('Forbidden')) {
    message = 'You do not have permission to access this resource.';
    type = 'warning';
  }

  const bgColor = type === 'error' ? 'bg-red-50' : 'bg-yellow-50';
  const textColor = type === 'error' ? 'text-red-800' : 'text-yellow-800';
  const borderColor = type === 'error' ? 'border-red-200' : 'border-yellow-200';

  return (
    <div className={`rounded-md ${bgColor} ${borderColor} p-4 border`}>
      <div className="flex">
        <div className="flex-shrink-0">
          {type === 'error' ? (
            <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          ) : (
            <svg className="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          )}
        </div>
        <div className="ml-3">
          <h3 className={`text-sm font-medium ${textColor}`}>
            {type === 'error' ? 'Error' : 'Warning'}
          </h3>
          <div className={`mt-2 text-sm ${textColor}`}>
            <p>{message}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ErrorHandler;