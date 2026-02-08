// 'use client'

// import { useState, useEffect } from 'react'
// import Link from 'next/link'
// import { usePathname } from 'next/navigation'

// interface SidebarProps {
//   children?: React.ReactNode
//   isOpen?: boolean
//   onToggle?: () => void
//   variant?: 'permanent' | 'temporary' | 'persistent'
// }

// export function Sidebar({
//   children,
//   isOpen: externalIsOpen,
//   onToggle,
//   variant = 'permanent'
// }: SidebarProps) {
//   const pathname = usePathname()
//   const [internalIsOpen, setInternalIsOpen] = useState(false)

//   // Use external state if provided, otherwise use internal state
//   const isOpen = externalIsOpen !== undefined ? externalIsOpen : internalIsOpen

//   // Close sidebar on route change when it's temporary
//   useEffect(() => {
//     if (variant === 'temporary') {
//       setInternalIsOpen(false)
//     }
//   }, [pathname, variant])

//   const toggleSidebar = () => {
//     if (onToggle) {
//       onToggle()
//     } else {
//       setInternalIsOpen(!internalIsOpen)
//     }
//   }

//   // Navigation items for the sidebar
//   const navItems = [
//     { name: 'Dashboard', href: '/dashboard', icon: DashboardIcon },
//     { name: 'Todos', href: '/todos', icon: TodoIcon },
//     { name: 'Calendar', href: '/calendar', icon: CalendarIcon },
//     { name: 'Team', href: '/team', icon: TeamIcon },
//     { name: 'Settings', href: '/settings', icon: SettingsIcon },
//   ]

//   return (
//     <>
//       {/* Mobile sidebar backdrop */}
//       {variant === 'temporary' && isOpen && (
//         <div
//           className="fixed inset-0 z-40 bg-black bg-opacity-50 md:hidden"
//           onClick={toggleSidebar}
//         />
//       )}

//       {/* Sidebar */}
//       <aside
//         className={`
//           fixed md:relative z-50 transform transition-transform duration-300 ease-in-out
//           h-full w-64 bg-white shadow-lg
//           ${variant === 'temporary' ?
//             `top-0 left-0 ${isOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0` :
//             'translate-x-0'
//           }
//           ${variant === 'persistent' && !isOpen ? '-translate-x-full md:translate-x-0 md:translate-x-0' : ''}
//           md:translate-x-0
//         `}
//       >
//         <div className="flex flex-col h-full">
//           {/* Sidebar header */}
//           <div className="flex items-center justify-between p-4 border-b">
//             <div className="flex items-center">
//               <div className="text-xl font-bold text-indigo-600">Todo App</div>
//             </div>
//             {variant === 'temporary' && (
//               <button
//                 onClick={toggleSidebar}
//                 className="md:hidden text-gray-500 hover:text-gray-700"
//               >
//                 <CloseIcon />
//               </button>
//             )}
//           </div>

//           {/* Sidebar navigation */}
//           <nav className="flex-1 px-2 py-4 overflow-y-auto">
//             <ul className="space-y-1">
//               {navItems.map((item) => {
//                 const isActive = pathname === item.href
//                 return (
//                   <li key={item.name}>
//                     <Link
//                       href={item.href}
//                       className={`
//                         flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors
//                         ${isActive
//                           ? 'bg-indigo-100 text-indigo-700'
//                           : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
//                         }
//                       `}
//                     >
//                       <item.icon className="mr-3 h-5 w-5" />
//                       <span>{item.name}</span>
//                     </Link>
//                   </li>
//                 )
//               })}
//             </ul>
//           </nav>

//           {/* Sidebar footer */}
//           <div className="p-4 border-t">
//             <div className="flex items-center">
//               <div className="flex-shrink-0">
//                 <div className="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center">
//                   <UserIcon />
//                 </div>
//               </div>
//               <div className="ml-3">
//                 <p className="text-sm font-medium text-gray-700">User Name</p>
//                 <p className="text-xs font-medium text-gray-500">user@example.com</p>
//               </div>
//             </div>
//           </div>
//         </div>
//       </aside>

//       {/* Temporary sidebar toggle button for mobile */}
//       {variant === 'temporary' && (
//         <button
//           className="md:hidden fixed top-4 left-4 z-40 p-2 rounded-md text-gray-500 bg-white shadow"
//           onClick={toggleSidebar}
//         >
//           <MenuIcon />
//         </button>
//       )}
//     </>
//   )
// }

// // Icon components
// interface IconProps {
//   className?: string;
// }

// function MenuIcon({ className = "h-6 w-6" }: IconProps) {
//   return (
//     <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
//       <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
//     </svg>
//   )
// }

// function CloseIcon({ className = "h-6 w-6" }: IconProps) {
//   return (
//     <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
//       <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
//     </svg>
//   )
// }

// function DashboardIcon({ className = "h-5 w-5" }: IconProps) {
//   return (
//     <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
//       <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
//     </svg>
//   )
// }

// function TodoIcon({ className = "h-5 w-5" }: IconProps) {
//   return (
//     <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
//       <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
//     </svg>
//   )
// }

// function CalendarIcon({ className = "h-5 w-5" }: IconProps) {
//   return (
//     <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
//       <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
//     </svg>
//   )
// }

// function TeamIcon({ className = "h-5 w-5" }: IconProps) {
//   return (
//     <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
//       <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
//     </svg>
//   )
// }

// function SettingsIcon({ className = "h-5 w-5" }: IconProps) {
//   return (
//     <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
//       <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
//       <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
//     </svg>
//   )
// }

// function UserIcon({ className = "h-6 w-6 text-indigo-500" }: IconProps) {
//   return (
//     <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
//       <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
//     </svg>
//   )
// }

'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

interface SidebarProps {
  children?: React.ReactNode
  isOpen?: boolean
  onToggle?: () => void
  variant?: 'permanent' | 'temporary' | 'persistent'
}

export function Sidebar({
  children,
  isOpen: externalIsOpen,
  onToggle,
  variant = 'permanent'
}: SidebarProps) {
  const pathname = usePathname()
  const [internalIsOpen, setInternalIsOpen] = useState(false)

  // Use external state if provided, otherwise use internal state
  const isOpen = externalIsOpen !== undefined ? externalIsOpen : internalIsOpen

  // Close sidebar on route change when it's temporary
  useEffect(() => {
    if (variant === 'temporary') {
      setInternalIsOpen(false)
    }
  }, [pathname, variant])

  const toggleSidebar = () => {
    if (onToggle) {
      onToggle()
    } else {
      setInternalIsOpen(!internalIsOpen)
    }
  }

  // Navigation items for the sidebar
  const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: DashboardIcon },
    { name: 'Todos', href: '/todos', icon: TodoIcon },
    { name: 'Calendar', href: '/calendar', icon: CalendarIcon },
    { name: 'Team', href: '/team', icon: TeamIcon },
    { name: 'Settings', href: '/settings', icon: SettingsIcon },
  ]

  return (
    <>
      {/* Mobile sidebar backdrop */}
      {variant === 'temporary' && isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm md:hidden transition-opacity duration-300"
          onClick={toggleSidebar}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed md:relative z-50 transform transition-all duration-300 ease-in-out
          h-full w-72 bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 shadow-2xl
          ${variant === 'temporary' ?
            `top-0 left-0 ${isOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0` :
            'translate-x-0'
          }
          ${variant === 'persistent' && !isOpen ? '-translate-x-full md:translate-x-0 md:translate-x-0' : ''}
          md:translate-x-0
        `}
      >
        <div className="flex flex-col h-full">
          {/* Sidebar header */}
          <div className="flex items-center justify-between p-6 border-b border-white/10">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <div className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
                Todo App
              </div>
            </div>
            {variant === 'temporary' && (
              <button
                onClick={toggleSidebar}
                className="md:hidden text-gray-400 hover:text-white p-2 rounded-lg hover:bg-white/10 transition-all duration-200"
              >
                <CloseIcon />
              </button>
            )}
          </div>

          {/* Sidebar navigation */}
          <nav className="flex-1 px-4 py-6 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-transparent">
            <ul className="space-y-2">
              {navItems.map((item) => {
                const isActive = pathname === item.href
                return (
                  <li key={item.name}>
                    <Link
                      href={item.href}
                      className={`
                        group flex items-center px-4 py-3 text-sm font-semibold rounded-xl transition-all duration-200
                        ${isActive
                          ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-500/50 scale-105'
                          : 'text-gray-300 hover:text-white hover:bg-white/10 hover:scale-105'
                        }
                      `}
                    >
                      <item.icon className={`mr-3 h-5 w-5 transition-transform duration-200 ${isActive ? '' : 'group-hover:scale-110'}`} />
                      <span>{item.name}</span>
                      {isActive && (
                        <span className="ml-auto">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                        </span>
                      )}
                    </Link>
                  </li>
                )
              })}
            </ul>
          </nav>

          {/* Sidebar footer */}
          <div className="p-4 border-t border-white/10 bg-black/20">
            <div className="flex items-center space-x-3 p-3 rounded-xl bg-white/5 hover:bg-white/10 transition-all duration-200 cursor-pointer group">
              <div className="flex-shrink-0">
                <div className="h-12 w-12 rounded-full bg-gradient-to-br from-pink-500 to-purple-600 flex items-center justify-center shadow-lg group-hover:shadow-xl group-hover:scale-105 transition-all duration-200">
                  <UserIcon />
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-white truncate">User Name</p>
                <p className="text-xs font-medium text-gray-400 truncate">user@example.com</p>
              </div>
              <svg className="w-5 h-5 text-gray-400 group-hover:text-white transition-colors duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        </div>
      </aside>

      {/* Temporary sidebar toggle button for mobile */}
      {variant === 'temporary' && (
        <button
          className="md:hidden fixed top-4 left-4 z-40 p-3 rounded-xl text-white bg-gradient-to-br from-indigo-600 to-purple-600 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-200"
          onClick={toggleSidebar}
        >
          <MenuIcon />
        </button>
      )}
    </>
  )
}

// Icon components
interface IconProps {
  className?: string;
}

function MenuIcon({ className = "h-6 w-6" }: IconProps) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  )
}

function CloseIcon({ className = "h-6 w-6" }: IconProps) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
    </svg>
  )
}

function DashboardIcon({ className = "h-5 w-5" }: IconProps) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
    </svg>
  )
}

function TodoIcon({ className = "h-5 w-5" }: IconProps) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
    </svg>
  )
}

function CalendarIcon({ className = "h-5 w-5" }: IconProps) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
    </svg>
  )
}

function TeamIcon({ className = "h-5 w-5" }: IconProps) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
    </svg>
  )
}

function SettingsIcon({ className = "h-5 w-5" }: IconProps) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  )
}

function UserIcon({ className = "h-6 w-6 text-white" }: IconProps) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
    </svg>
  )
}