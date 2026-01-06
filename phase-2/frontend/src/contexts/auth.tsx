'use client'

import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { useRouter } from 'next/navigation'
import * as authService from '@/services/auth'

interface AuthContextType {
  isAuthenticated: boolean
  user: any
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  register: (userData: { email: string; password: string; username?: string; first_name?: string; last_name?: string }) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    // Check if user is authenticated on initial load
    const initAuth = async () => {
      try {
        if (authService.isAuthenticated()) {
          setIsAuthenticated(true)
          const userData = await authService.getProfile()
          setUser(userData)
        }
      } catch (error) {
        console.error('Error initializing auth:', error)
        localStorage.removeItem('access_token')
        localStorage.removeItem('token')
      } finally {
        setIsLoading(false)
      }
    }

    initAuth()
  }, [])

  const login = async (email: string, password: string) => {
    try {
      const response = await authService.login({ email, password })
      if (response) {
        setIsAuthenticated(true)
        setUser(response.user || response)
        router.push('/dashboard')
      } else {
        throw new Error('Login failed')
      }
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  }

  const register = async (userData: { email: string; password: string; username?: string; first_name?: string; last_name?: string }) => {
    try {
      const response = await authService.register(userData)
      if (response) {
        setIsAuthenticated(true)
        setUser(response.user || response)
        router.push('/dashboard')
      } else {
        throw new Error('Registration failed')
      }
    } catch (error) {
      console.error('Registration error:', error)
      throw error
    }
  }

  const logout = async () => {
    try {
      await authService.logout()
    } catch (error) {
      console.error('Logout error:', error)
      // Even if the server logout fails, we still clear the client-side token
    } finally {
      setIsAuthenticated(false)
      setUser(null)
      router.push('/login')
    }
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, isLoading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}