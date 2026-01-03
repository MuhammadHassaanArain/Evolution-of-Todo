import React from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import SignupForm from '../components/auth/SignupForm';
import { useAuth } from '../lib/better-auth-client';

const SignupPage: NextPage = () => {
  const { useAuth: useAuthHook } = useAuth;
  const { user } = useAuthHook();

  // If user is already authenticated, redirect to dashboard
  if (user) {
    // In a real app, you might want to use Next.js router to redirect
    // For now, we'll just show a message
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Already Signed In
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              You are already signed in. Visit the dashboard to manage your tasks.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Head>
        <title>Sign Up | Todo App</title>
        <meta name="description" content="Create a new account" />
      </Head>

      <SignupForm />
    </div>
  );
};

export default SignupPage;