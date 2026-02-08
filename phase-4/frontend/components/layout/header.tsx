'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useAuth } from '@/contexts/auth'

export function Header() {
  const pathname = usePathname()
  const { isAuthenticated, user, logout } = useAuth()

  const handleLogout = async () => {
    try {
      await logout()
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  return (
    <header className="bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-700 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-8">
            <Link 
              href="/" 
              className="text-2xl font-extrabold text-white hover:text-indigo-100 transition-colors duration-200 flex items-center space-x-2"
            >
              <svg 
                className="w-8 h-8" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" 
                />
              </svg>
              <span>Todo App</span>
            </Link>
            <nav className="hidden md:block">
              <div className="flex space-x-2">
                <Link
                  href="/"
                  className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 ${
                    pathname === '/'
                      ? 'bg-white text-indigo-700 shadow-md'
                      : 'text-white hover:bg-white/20 hover:shadow-sm'
                  }`}
                >
                  Home
                </Link>
                {isAuthenticated && (
                  <>
                    <Link
                      href="/dashboard"
                      className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 ${
                        pathname === '/dashboard'
                          ? 'bg-white text-indigo-700 shadow-md'
                          : 'text-white hover:bg-white/20 hover:shadow-sm'
                      }`}
                    >
                      Dashboard
                    </Link>
                    <Link
                      href="/todos"
                      className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 ${
                        pathname === '/todos'
                          ? 'bg-white text-indigo-700 shadow-md'
                          : 'text-white hover:bg-white/20 hover:shadow-sm'
                      }`}
                    >
                      Todos
                    </Link>
                  </>
                )}
              </div>
            </nav>
          </div>
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <div className="hidden sm:flex items-center space-x-3 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full border border-white/20">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-pink-400 to-purple-500 flex items-center justify-center text-white font-bold text-sm shadow-md">
                    <Link href={"/profile"}>{(user?.username?.[0] || user?.email?.[0] || 'U').toUpperCase()}</Link>
                  </div>
                  <span className="text-sm font-medium text-white">
                    {user?.username || user?.email || 'User'}
                  </span>
                </div>
                <button
                  onClick={handleLogout}
                  className="px-5 py-2 text-sm font-semibold text-white bg-red-500 rounded-lg hover:bg-red-600 shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-200"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <Link
                  href="/login"
                  className="px-4 py-2 text-sm font-semibold text-white hover:text-indigo-100 transition-colors duration-200"
                >
                  Sign In
                </Link>
                <Link
                  href="/signup"
                  className="px-5 py-2 text-sm font-semibold text-indigo-600 bg-white rounded-lg hover:bg-indigo-50 shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-200"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}