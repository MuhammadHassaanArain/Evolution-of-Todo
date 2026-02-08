import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Breakpoint values in pixels
export const BREAKPOINTS = {
  sm: 640,   // Mobile
  md: 768,   // Tablet
  lg: 1024,  // Desktop
  xl: 1280,  // Large Desktop
  '2xl': 1536 // Extra Large
} as const

export type Breakpoint = keyof typeof BREAKPOINTS

// Responsive utility functions
export function isMobile() {
  if (typeof window === 'undefined') return false
  return window.innerWidth < BREAKPOINTS.md
}

export function isTablet() {
  if (typeof window === 'undefined') return false
  return window.innerWidth >= BREAKPOINTS.md && window.innerWidth < BREAKPOINTS.lg
}

export function isDesktop() {
  if (typeof window === 'undefined') return false
  return window.innerWidth >= BREAKPOINTS.lg
}

// Function to get the current breakpoint
export function getCurrentBreakpoint(): Breakpoint | null {
  if (typeof window === 'undefined') return null

  const width = window.innerWidth

  if (width < BREAKPOINTS.md) return 'sm'
  if (width < BREAKPOINTS.lg) return 'md'
  if (width < BREAKPOINTS.xl) return 'lg'
  if (width < BREAKPOINTS['2xl']) return 'xl'
  return '2xl'
}

// Function to check if current screen matches a breakpoint or larger
export function matchesBreakpoint(bp: Breakpoint): boolean {
  if (typeof window === 'undefined') return false

  const bpValue = BREAKPOINTS[bp]
  return window.innerWidth >= bpValue
}