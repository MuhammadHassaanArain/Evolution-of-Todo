import { ReactNode } from 'react'

interface ContainerProps {
  children: ReactNode
  className?: string
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl' | '6xl' | '7xl'
}

export function Container({
  children,
  className = '',
  maxWidth = '7xl'
}: ContainerProps) {
  const maxWidthClass = `max-w-${maxWidth}`

  return (
    <div className={`mx-auto px-4 sm:px-6 lg:px-8 ${maxWidthClass} ${className}`}>
      {children}
    </div>
  )
}

// Responsive container that adjusts padding based on screen size
interface ResponsiveContainerProps {
  children: ReactNode
  className?: string
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl' | '6xl' | '7xl'
  padding?: boolean
}

export function ResponsiveContainer({
  children,
  className = '',
  maxWidth = '7xl',
  padding = true
}: ResponsiveContainerProps) {
  const maxWidthClass = `max-w-${maxWidth}`
  const paddingClass = padding ? 'px-4 sm:px-6 lg:px-8' : ''

  return (
    <div className={`mx-auto ${maxWidthClass} ${paddingClass} ${className}`}>
      {children}
    </div>
  )
}

// Flex container with responsive gap
interface FlexContainerProps {
  children: ReactNode
  className?: string
  direction?: 'row' | 'col' | 'row-reverse' | 'col-reverse'
  justifyContent?: 'start' | 'center' | 'end' | 'between' | 'around' | 'evenly'
  alignItems?: 'start' | 'center' | 'end' | 'stretch' | 'baseline'
  gap?: '0' | '1' | '2' | '3' | '4' | '5' | '6' | '8' | '10' | '12' | '16'
}

export function FlexContainer({
  children,
  className = '',
  direction = 'row',
  justifyContent = 'start',
  alignItems = 'stretch',
  gap = '4'
}: FlexContainerProps) {
  const directionClass = `flex-${direction.replace('-', '')}`
  const justifyContentClass = `justify-${justifyContent}`
  const alignItemsClass = `items-${alignItems}`
  const gapClass = `gap-${gap}`

  return (
    <div
      className={`flex ${directionClass} ${justifyContentClass} ${alignItemsClass} ${gapClass} ${className}`}
    >
      {children}
    </div>
  )
}

// Grid container with responsive columns
interface GridContainerProps {
  children: ReactNode
  className?: string
  cols?: '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | '11' | '12'
  gap?: '0' | '1' | '2' | '3' | '4' | '5' | '6' | '8' | '10' | '12' | '16'
  responsive?: boolean
}

export function GridContainer({
  children,
  className = '',
  cols = '1',
  gap = '4',
  responsive = true
}: GridContainerProps) {
  const colsClass = responsive
    ? `grid-cols-1 sm:grid-cols-${cols} md:grid-cols-${cols} lg:grid-cols-${cols}`
    : `grid-cols-${cols}`
  const gapClass = `gap-${gap}`

  return (
    <div
      className={`grid ${colsClass} ${gapClass} ${className}`}
    >
      {children}
    </div>
  )
}