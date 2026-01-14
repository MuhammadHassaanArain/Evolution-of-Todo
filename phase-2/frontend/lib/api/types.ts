/**
 * API response and request types
 */

// Common API response structure
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: ApiError;
}

// API error structure
export interface ApiError {
  code: string;
  message: string;
  details?: any;
}

// User data structure
export interface User {
  id: number;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  created_at: string; // ISO 8601 date string
  updated_at: string; // ISO 8601 date string
}

// Todo data structure
export interface Todo {
  id: number;
  title: string;
  description?: string;
  is_completed: boolean;
  owner_id: number;
  created_at: string; // ISO 8601 date string
  updated_at: string; // ISO 8601 date string
}

// Login request/response
export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

// Registration request/response
export interface RegisterRequest {
  email: string;
  password: string;
  username: string;
  first_name?: string;
  last_name?: string;
}

export interface RegisterResponse extends User {}

// API client options
export interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  headers?: Record<string, string>;
  body?: any;
  requiresAuth?: boolean;
}

// Auth session interface
export interface AuthSession {
  token: string;
  expiresAt: Date;
  userId: string;
  isAuthenticated: boolean;
}

// Route interface
export interface Route {
  path: string;
  isProtected: boolean;
  redirectPath?: string;
  component: React.ComponentType;
}