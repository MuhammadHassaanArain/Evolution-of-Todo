/**
 * Environment configuration management
 */

interface EnvironmentConfig {
  apiUrl: string;
  jwtSecret: string;
  environment: 'development' | 'production' | 'test';
}

// Default configuration
const defaultConfig: EnvironmentConfig = {
  apiUrl: 'http://localhost:8000',
  jwtSecret: 'your-jwt-secret-for-validation',
  environment: 'development',
};

// Production overrides
const productionConfig: EnvironmentConfig = {
  apiUrl: 'https://api.todoapp.com',
  jwtSecret: process.env.NEXT_PUBLIC_JWT_SECRET || 'fallback-jwt-secret',
  environment: 'production',
};

// Test overrides
const testConfig: EnvironmentConfig = {
  apiUrl: 'http://localhost:8000',
  jwtSecret: 'test-jwt-secret',
  environment: 'test',
};

/**
 * Gets the current environment configuration
 * @returns EnvironmentConfig object with appropriate values for current environment
 */
export function getEnvironmentConfig(): EnvironmentConfig {
  const env = process.env.NODE_ENV || 'development';

  switch (env) {
    case 'production':
      return {
        ...defaultConfig,
        ...productionConfig,
      };
    case 'test':
      return {
        ...defaultConfig,
        ...testConfig,
      };
    default:
      return defaultConfig;
  }
}

/**
 * Gets the API base URL based on current environment
 * @returns API base URL string
 */
export function getApiBaseUrl(): string {
  return getEnvironmentConfig().apiUrl;
}

/**
 * Gets the JWT secret for token validation
 * @returns JWT secret string
 */
export function getJwtSecret(): string {
  return getEnvironmentConfig().jwtSecret;
}

/**
 * Checks if the current environment is production
 * @returns Boolean indicating if environment is production
 */
export function isProduction(): boolean {
  return getEnvironmentConfig().environment === 'production';
}

/**
 * Checks if the current environment is development
 * @returns Boolean indicating if environment is development
 */
export function isDevelopment(): boolean {
  return getEnvironmentConfig().environment === 'development';
}

/**
 * Checks if the current environment is test
 * @returns Boolean indicating if environment is test
 */
export function isTest(): boolean {
  return getEnvironmentConfig().environment === 'test';
}