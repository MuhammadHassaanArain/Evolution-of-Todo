import { useState, useEffect } from 'react'

// Define breakpoints
export const BREAKPOINTS = {
  sm: 640,   // Mobile: 640px and above
  md: 768,   // Tablet: 768px and above
  lg: 1024,  // Desktop: 1024px and above
  xl: 1280,  // Large Desktop: 1280px and above
  '2xl': 1536 // Extra Large Desktop: 1536px and above
} as const

export type Breakpoint = keyof typeof BREAKPOINTS

// Hook to check if the current viewport matches a breakpoint
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false)

  useEffect(() => {
    if (typeof window === 'undefined') {
      return
    }

    const media = window.matchMedia(query)

    // Set initial value
    if (media.matches !== matches) {
      setMatches(media.matches)
    }

    // Listen for changes
    const listener = () => setMatches(media.matches)
    media.addEventListener('change', listener)

    return () => media.removeEventListener('change', listener)
  }, [matches, query])

  return matches
}

// Specific hooks for common breakpoints
export function useIsMobile(): boolean {
  return useMediaQuery('(max-width: 639px)')
}

export function useIsTablet(): boolean {
  return useMediaQuery('(min-width: 640px) and (max-width: 767px)')
}

export function useIsDesktop(): boolean {
  return useMediaQuery('(min-width: 768px) and (max-width: 1023px)')
}

export function useIsLargeDesktop(): boolean {
  return useMediaQuery('(min-width: 1024px)')
}

// Hook to get the current breakpoint
export function useCurrentBreakpoint(): Breakpoint | null {
  const isSm = useMediaQuery('(min-width: 640px)')
  const isMd = useMediaQuery('(min-width: 768px)')
  const isLg = useMediaQuery('(min-width: 1024px)')
  const isXl = useMediaQuery('(min-width: 1280px)')
  const is2Xl = useMediaQuery('(min-width: 1536px)')

  if (is2Xl) return '2xl'
  if (isXl) return 'xl'
  if (isLg) return 'lg'
  if (isMd) return 'md'
  if (isSm) return 'sm'

  return null // Mobile
}

// Hook to check if the current screen matches a specific breakpoint or larger
export function useBreakpoint(breakpoint: Breakpoint): boolean {
  const breakpointValue = BREAKPOINTS[breakpoint]
  return useMediaQuery(`(min-width: ${breakpointValue}px)`)
}

// Hook to check if the current screen is smaller than a specific breakpoint
export function useBreakpointDown(breakpoint: Breakpoint): boolean {
  const breakpointValue = BREAKPOINTS[breakpoint]
  return useMediaQuery(`(max-width: ${breakpointValue - 1}px)`)
}

// Hook to check if the current screen is between two breakpoints
export function useBreakpointBetween(lower: Breakpoint, upper: Breakpoint): boolean {
  const lowerValue = BREAKPOINTS[lower]
  const upperValue = BREAKPOINTS[upper]
  return useMediaQuery(`(min-width: ${lowerValue}px) and (max-width: ${upperValue - 1}px)`)
}

// Hook to get the current viewport dimensions
export function useViewportSize(): { width: number; height: number } {
  const [size, setSize] = useState({ width: 0, height: 0 })

  useEffect(() => {
    if (typeof window === 'undefined') {
      return
    }

    const updateSize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight
      })
    }

    // Set initial size
    updateSize()

    // Add event listener
    window.addEventListener('resize', updateSize)

    // Cleanup
    return () => window.removeEventListener('resize', updateSize)
  }, [])

  return size
}

// Hook to check if user prefers reduced motion
export function usePrefersReducedMotion(): boolean {
  return useMediaQuery('(prefers-reduced-motion: reduce)')
}

// Hook to check if user prefers dark mode
export function usePrefersDarkMode(): boolean {
  return useMediaQuery('(prefers-color-scheme: dark)')
}

// Hook to check if user prefers light mode
export function usePrefersLightMode(): boolean {
  return useMediaQuery('(prefers-color-scheme: light)')
}

// Hook to check if user prefers contrast
export function usePrefersContrast(): boolean {
  return useMediaQuery('(prefers-contrast: more)')
}