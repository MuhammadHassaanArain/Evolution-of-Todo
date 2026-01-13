// 'use client'

// import { useState, useEffect } from 'react'
// import Link from 'next/link'
// import { usePathname } from 'next/navigation'

// export function Navigation() {
//   const [isMenuOpen, setIsMenuOpen] = useState(false)
//   const pathname = usePathname()

//   // Close menu when route changes
//   useEffect(() => {
//     setIsMenuOpen(false)
//   }, [pathname])

//   const navItems = [
//     { name: 'Home', href: '/' },
//     { name: 'Dashboard', href: '/dashboard' },
//     { name: 'Todos', href: '/todos' },
//   ]

//   return (
//     <nav className="bg-white shadow">
//       <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
//         <div className="flex justify-between h-16">
//           <div className="flex items-center">
//             <div className="flex-shrink-0 flex items-center">
//               <Link href="/" className="text-xl font-bold text-indigo-600">
//                 Todo App
//               </Link>
//             </div>
//             <div className="hidden md:ml-6 md:flex md:space-x-8">
//               {navItems.map((item) => (
//                 <Link
//                   key={item.name}
//                   href={item.href}
//                   className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
//                     pathname === item.href
//                       ? 'border-indigo-500 text-gray-900'
//                       : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
//                   }`}
//                 >
//                   {item.name}
//                 </Link>
//               ))}
//             </div>
//           </div>
//           <div className="flex items-center md:hidden">
//             {/* Mobile menu button */}
//             <button
//               type="button"
//               className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
//               onClick={() => setIsMenuOpen(!isMenuOpen)}
//               aria-expanded="false"
//               aria-controls="mobile-menu"
//             >
//               <span className="sr-only">Open main menu</span>
//               <svg
//                 className={`${isMenuOpen ? 'hidden' : 'block'} h-6 w-6`}
//                 xmlns="http://www.w3.org/2000/svg"
//                 fill="none"
//                 viewBox="0 0 24 24"
//                 stroke="currentColor"
//                 aria-hidden="true"
//               >
//                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
//               </svg>
//               <svg
//                 className={`${isMenuOpen ? 'block' : 'hidden'} h-6 w-6`}
//                 xmlns="http://www.w3.org/2000/svg"
//                 fill="none"
//                 viewBox="0 0 24 24"
//                 stroke="currentColor"
//                 aria-hidden="true"
//               >
//                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
//               </svg>
//             </button>
//           </div>
//           <div className="hidden md:flex items-center">
//             <Link
//               href="/sign-in"
//               className="ml-4 px-3 py-2 text-sm font-medium text-gray-700 hover:text-indigo-600"
//             >
//               Sign In
//             </Link>
//             <Link
//               href="/sign-up"
//               className="ml-4 px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700"
//             >
//               Sign Up
//             </Link>
//           </div>
//         </div>
//       </div>

//       {/* Mobile menu */}
//       {isMenuOpen && (
//         <div className="md:hidden" id="mobile-menu">
//           <div className="pt-2 pb-3 space-y-1">
//             {navItems.map((item) => (
//               <Link
//                 key={item.name}
//                 href={item.href}
//                 className={`${
//                   pathname === item.href
//                     ? 'bg-indigo-50 border-indigo-500 text-indigo-700'
//                     : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700'
//                 } block pl-3 pr-4 py-2 border-l-4 text-base font-medium`}
//               >
//                 {item.name}
//               </Link>
//             ))}
//           </div>
//           <div className="pt-4 pb-3 border-t border-gray-200">
//             <div className="flex items-center px-4 space-x-3">
//               <Link
//                 href="/sign-in"
//                 className="w-full px-3 py-2 text-base font-medium text-gray-700 hover:text-indigo-600 text-center"
//               >
//                 Sign In
//               </Link>
//               <Link
//                 href="/sign-up"
//                 className="w-full px-4 py-2 text-base font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 text-center"
//               >
//                 Sign Up
//               </Link>
//             </div>
//           </div>
//         </div>
//       )}
//     </nav>
//   )
// }

'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

export function Navigation() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const pathname = usePathname()

  // Close menu when route changes
  useEffect(() => {
    setIsMenuOpen(false)
  }, [pathname])

  const navItems = [
    { name: 'Home', href: '/' },
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Todos', href: '/todos' },
  ]

  return (
    <nav className="bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-700 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center">
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
            </div>
            <div className="hidden md:ml-8 md:flex md:space-x-2">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 ${
                    pathname === item.href
                      ? 'bg-white text-indigo-700 shadow-md'
                      : 'text-white hover:bg-white/20 hover:shadow-sm'
                  }`}
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
          <div className="flex items-center md:hidden">
            {/* Mobile menu button */}
            <button
              type="button"
              className="inline-flex items-center justify-center p-2 rounded-lg text-white hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white/50 transition-all duration-200"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-expanded="false"
              aria-controls="mobile-menu"
            >
              <span className="sr-only">Open main menu</span>
              <svg
                className={`${isMenuOpen ? 'hidden' : 'block'} h-6 w-6`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg
                className={`${isMenuOpen ? 'block' : 'hidden'} h-6 w-6`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div className="hidden md:flex items-center space-x-3">
            <Link
              href="/sign-in"
              className="px-4 py-2 text-sm font-semibold text-white hover:text-indigo-100 transition-colors duration-200"
            >
              Sign In
            </Link>
            <Link
              href="/sign-up"
              className="px-5 py-2 text-sm font-semibold text-indigo-600 bg-white rounded-lg hover:bg-indigo-50 shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-200"
            >
              Sign Up
            </Link>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-white/10 backdrop-blur-md border-t border-white/20" id="mobile-menu">
          <div className="pt-2 pb-3 space-y-1 px-3">
            {navItems.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={`${
                  pathname === item.href
                    ? 'bg-white text-indigo-700 shadow-md'
                    : 'text-white hover:bg-white/20'
                } block px-4 py-3 rounded-lg text-base font-semibold transition-all duration-200`}
              >
                {item.name}
              </Link>
            ))}
          </div>
          <div className="pt-4 pb-3 border-t border-white/20">
            <div className="flex flex-col px-3 space-y-2">
              <Link
                href="/sign-in"
                className="w-full px-4 py-2 text-base font-semibold text-white hover:bg-white/20 rounded-lg text-center transition-all duration-200"
              >
                Sign In
              </Link>
              <Link
                href="/sign-up"
                className="w-full px-4 py-2 text-base font-semibold text-indigo-600 bg-white rounded-lg hover:bg-indigo-50 shadow-md text-center transition-all duration-200"
              >
                Sign Up
              </Link>
            </div>
          </div>
        </div>
      )}
    </nav>
  )
}