/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1',
    NEXT_PUBLIC_JWT_SECRET: process.env.NEXT_PUBLIC_JWT_SECRET || 'your-jwt-secret-for-validation',
  },
  images: {
    domains: ['localhost', 'api.todoapp.com'],
  },
  async redirects() {
    return [
      // Redirect from root to login if not authenticated
      // This would need to be handled client-side since we need auth state
    ]
  }
}

module.exports = nextConfig