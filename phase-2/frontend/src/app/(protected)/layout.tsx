'use client'

import { useAuth } from '@/contexts/auth'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const { isAuthenticated, user } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, router])

  if (!isAuthenticated) {
    return <div>Redirecting...</div>
  }

  return (
    <div>
      {children}
    </div>
  )
}