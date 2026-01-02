import React from 'react';
import LoginForm from '../../components/auth/LoginForm';

const LoginPage = () => {
  const handleLogin = (user) => {
    console.log('User logged in:', user);
    // Handle successful login (e.g., update context, redirect, etc.)
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your Todo account
          </h2>
        </div>
        <LoginForm onLogin={handleLogin} />
        <div className="text-center mt-4">
          <p className="text-sm text-gray-600">
            Don't have an account?{' '}
            <a href="/register" className="font-medium text-indigo-600 hover:text-indigo-500">
              Sign up
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;