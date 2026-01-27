'use client'

import { useState, Suspense } from 'react'
import { useAuth } from '@/contexts/auth'
import { useRouter, useSearchParams } from 'next/navigation'

// Separate component for handling search params to avoid SSR issues
function LoginFormContent() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const router = useRouter()
  const searchParams = useSearchParams()
  const redirect = searchParams?.get('redirect') || '/dashboard'

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await login(email, password)
      router.push(redirect)
    } catch (err) {
      setError('Invalid email or password')
      console.error('Login error:', err)
    }
  }

  return (
    <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <p className="text-sm font-medium text-red-800">{error}</p>
        </div>
      )}
      <input type="hidden" name="remember" defaultValue="true" />
      <div className="rounded-md shadow-sm -space-y-px">
        <div>
          <label htmlFor="email-address" className="sr-only">
            Email address
          </label>
          <input
            id="email-address"
            name="email"
            type="email"
            autoComplete="email"
            required
            className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
            placeholder="Email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password" className="sr-only">
            Password
          </label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
      </div>

      <div>
        <button
          type="submit"
          className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Sign in
        </button>
      </div>
    </form>
  )
}

function LoginForm() {
  return <Suspense fallback={<div>Loading...</div>}>
    <LoginFormContent />
  </Suspense>
}

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
        </div>
        <LoginForm />
      </div>
    </div>
  )
}



// 'use client'

// import { useState } from 'react'
// import { Mail, Lock, Eye, EyeOff, CheckSquare, AlertCircle } from 'lucide-react'

// // Mock hooks for demo
// const useAuth = () => ({
//   login: async (email: string, password: string) => {
//     await new Promise(resolve => setTimeout(resolve, 1000))
//     if (email === 'test@test.com' && password === 'password') {
//       return true
//     }
//     throw new Error('Invalid credentials')
//   }
// })

// const useRouter = () => ({
//   push: (path: string) => console.log('Navigate to:', path)
// })

// function LoginFormContent() {
//   const [email, setEmail] = useState('')
//   const [password, setPassword] = useState('')
//   const [error, setError] = useState('')
//   const [isLoading, setIsLoading] = useState(false)
//   const [showPassword, setShowPassword] = useState(false)
//   const { login } = useAuth()
//   const router = useRouter()

//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault()
//     setError('')
//     setIsLoading(true)
    
//     try {
//       await login(email, password)
//       router.push('/dashboard')
//     } catch (err) {
//       setError('Invalid email or password. Please try again.')
//       console.error('Login error:', err)
//     } finally {
//       setIsLoading(false)
//     }
//   }

//   return (
//     <div className="mt-8 space-y-6">
//       {error && (
//         <div className="rounded-xl bg-red-50 border border-red-200 p-4 flex items-start gap-3 animate-shake">
//           <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
//           <p className="text-sm font-medium text-red-800">{error}</p>
//         </div>
//       )}

//       <div className="space-y-4">
//         {/* Email Input */}
//         <div>
//           <label htmlFor="email-address" className="block text-sm font-semibold text-gray-700 mb-2">
//             Email Address
//           </label>
//           <div className="relative">
//             <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
//               <Mail className="h-5 w-5 text-gray-400" />
//             </div>
//             <input
//               id="email-address"
//               name="email"
//               type="email"
//               autoComplete="email"
//               required
//               className="block w-full pl-12 pr-4 py-3.5 border border-gray-300 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 bg-white hover:border-gray-400"
//               placeholder="Enter your email"
//               value={email}
//               onChange={(e) => setEmail(e.target.value)}
//             />
//           </div>
//         </div>

//         {/* Password Input */}
//         <div>
//           <label htmlFor="password" className="block text-sm font-semibold text-gray-700 mb-2">
//             Password
//           </label>
//           <div className="relative">
//             <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
//               <Lock className="h-5 w-5 text-gray-400" />
//             </div>
//             <input
//               id="password"
//               name="password"
//               type={showPassword ? 'text' : 'password'}
//               autoComplete="current-password"
//               required
//               className="block w-full pl-12 pr-12 py-3.5 border border-gray-300 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 bg-white hover:border-gray-400"
//               placeholder="Enter your password"
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//             />
//             <button
//               type="button"
//               onClick={() => setShowPassword(!showPassword)}
//               className="absolute inset-y-0 right-0 pr-4 flex items-center"
//             >
//               {showPassword ? (
//                 <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-600 transition-colors" />
//               ) : (
//                 <Eye className="h-5 w-5 text-gray-400 hover:text-gray-600 transition-colors" />
//               )}
//             </button>
//           </div>
//         </div>
//       </div>

//       {/* Remember & Forgot */}
//       <div className="flex items-center justify-between">
//         <div className="flex items-center">
//           <input
//             id="remember-me"
//             name="remember-me"
//             type="checkbox"
//             className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded cursor-pointer"
//           />
//           <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-700 cursor-pointer">
//             Remember me
//           </label>
//         </div>

//         <div className="text-sm">
//           <a href="#" className="font-semibold text-indigo-600 hover:text-indigo-500 transition-colors">
//             Forgot password?
//           </a>
//         </div>
//       </div>

//       {/* Submit Button */}
//       <div>
//         <button
//           type="button"
//           onClick={handleSubmit}
//           disabled={isLoading}
//           className="group relative w-full flex justify-center items-center gap-2 py-3.5 px-4 border border-transparent text-sm font-semibold rounded-xl text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
//         >
//           {isLoading ? (
//             <>
//               <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
//               Signing in...
//             </>
//           ) : (
//             <>
//               Sign in
//               <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
//               </svg>
//             </>
//           )}
//         </button>
//       </div>

//       {/* Divider */}
//       <div className="relative">
//         <div className="absolute inset-0 flex items-center">
//           <div className="w-full border-t border-gray-300"></div>
//         </div>
//         <div className="relative flex justify-center text-sm">
//           <span className="px-4 bg-white text-gray-500 font-medium">or continue with</span>
//         </div>
//       </div>

//       {/* Social Login Buttons */}
//       <div className="grid grid-cols-2 gap-3">
//         <button
//           type="button"
//           className="flex items-center justify-center gap-2 px-4 py-3 border border-gray-300 rounded-xl text-sm font-semibold text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200"
//         >
//           <svg className="w-5 h-5" viewBox="0 0 24 24">
//             <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
//             <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
//             <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
//             <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
//           </svg>
//           Google
//         </button>
//         <button
//           type="button"
//           className="flex items-center justify-center gap-2 px-4 py-3 border border-gray-300 rounded-xl text-sm font-semibold text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200"
//         >
//           <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
//             <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
//           </svg>
//           GitHub
//         </button>
//       </div>

//       {/* Sign Up Link */}
//       <div className="text-center">
//         <p className="text-sm text-gray-600">
//           Don't have an account?{' '}
//           <a href="/signup" className="font-semibold text-indigo-600 hover:text-indigo-500 transition-colors">
//             Sign up for free
//           </a>
//         </p>
//       </div>
//     </div>
//   )
// }

// export default function LoginPage() {
//   return (
//     <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 relative overflow-hidden">
//       {/* Animated background elements */}
//       <div className="absolute inset-0 overflow-hidden pointer-events-none">
//         <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
//         <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
//         <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-indigo-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
//       </div>

//       <div className="relative z-10 flex items-center justify-center min-h-screen py-12 px-4 sm:px-6 lg:px-8">
//         <div className="max-w-md w-full">
//           {/* Logo and Header */}
//           <div className="text-center mb-8">
//             <div className="flex justify-center mb-6">
//               <div className="w-16 h-16 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg transform hover:scale-110 transition-transform duration-300">
//                 <CheckSquare className="w-9 h-9 text-white" />
//               </div>
//             </div>
//             <h2 className="text-4xl font-bold text-gray-900 mb-2">
//               Welcome back
//             </h2>
//             <p className="text-gray-600">
//               Sign in to continue to TodoMaster
//             </p>
//           </div>

//           {/* Login Form Card */}
//           <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8">
//             <LoginFormContent />
//           </div>

//           {/* Footer */}
//           <div className="mt-8 text-center">
//             <p className="text-sm text-gray-600">
//               Protected by industry-standard encryption
//             </p>
//           </div>
//         </div>
//       </div>

//       <style jsx>{`
//         @keyframes blob {
//           0%, 100% { transform: translate(0, 0) scale(1); }
//           33% { transform: translate(30px, -50px) scale(1.1); }
//           66% { transform: translate(-20px, 20px) scale(0.9); }
//         }
//         .animate-blob {
//           animation: blob 7s infinite;
//         }
//         .animation-delay-2000 {
//           animation-delay: 2s;
//         }
//         .animation-delay-4000 {
//           animation-delay: 4s;
//         }
//         @keyframes shake {
//           0%, 100% { transform: translateX(0); }
//           10%, 30%, 50%, 70%, 90% { transform: translateX(-4px); }
//           20%, 40%, 60%, 80% { transform: translateX(4px); }
//         }
//         .animate-shake {
//           animation: shake 0.5s;
//         }
//       `}</style>
//     </div>
//   )
// }