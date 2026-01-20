import { ReactNode } from 'react'

interface GridProps {
  children: ReactNode
  className?: string
  cols?: number
  gap?: '0' | '1' | '2' | '3' | '4' | '5' | '6' | '8' | '10' | '12' | '16'
  smCols?: number
  mdCols?: number
  lgCols?: number
  xlCols?: number
}

export function Grid({
  children,
  className = '',
  cols = 1,
  gap = '4',
  smCols,
  mdCols,
  lgCols,
  xlCols
}: GridProps) {
  // Build responsive classes
  const colClasses = [
    `grid-cols-${cols}`, // Default (mobile)
    smCols ? `sm:grid-cols-${smCols}` : '',
    mdCols ? `md:grid-cols-${mdCols}` : '',
    lgCols ? `lg:grid-cols-${lgCols}` : '',
    xlCols ? `xl:grid-cols-${xlCols}` : ''
  ].filter(Boolean).join(' ')

  const gapClass = `gap-${gap}`

  return (
    <div className={`grid ${colClasses} ${gapClass} ${className}`}>
      {children}
    </div>
  )
}

// Grid item component for fine-grained control
interface GridItemProps {
  children: ReactNode
  className?: string
  colSpan?: number
  rowSpan?: number
  smColSpan?: number
  mdColSpan?: number
  lgColSpan?: number
  xlColSpan?: number
  alignSelf?: 'start' | 'end' | 'center' | 'stretch' | 'baseline'
  justifySelf?: 'start' | 'end' | 'center' | 'stretch'
}

export function GridItem({
  children,
  className = '',
  colSpan,
  rowSpan,
  smColSpan,
  mdColSpan,
  lgColSpan,
  xlColSpan,
  alignSelf,
  justifySelf
}: GridItemProps) {
  const spanClasses = [
    colSpan ? `col-span-${colSpan}` : '',
    smColSpan ? `sm:col-span-${smColSpan}` : '',
    mdColSpan ? `md:col-span-${mdColSpan}` : '',
    lgColSpan ? `lg:col-span-${lgColSpan}` : '',
    xlColSpan ? `xl:col-span-${xlColSpan}` : ''
  ].filter(Boolean).join(' ')

  const rowSpanClass = rowSpan ? `row-span-${rowSpan}` : ''

  const alignSelfClass = alignSelf ? `self-${alignSelf}` : ''
  const justifySelfClass = justifySelf ? `justify-self-${justifySelf}` : ''

  return (
    <div className={`${spanClasses} ${rowSpanClass} ${alignSelfClass} ${justifySelfClass} ${className}`}>
      {children}
    </div>
  )
}

// Responsive grid for card layouts
interface CardGridProps {
  children: ReactNode
  className?: string
  cols?: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12
  gap?: '0' | '1' | '2' | '3' | '4' | '5' | '6' | '8' | '10' | '12' | '16'
}

export function CardGrid({
  children,
  className = '',
  cols = 1,
  gap = '6'
}: CardGridProps) {
  // Mobile-first: 1 column, then 2 at small, 3 at medium, and specified at large
  const colClasses = `grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-${cols}`
  const gapClass = `gap-${gap}`

  return (
    <div className={`grid ${colClasses} ${gapClass} ${className}`}>
      {children}
    </div>
  )
}

// Auto-fit grid for flexible card layouts
interface AutoFitGridProps {
  children: ReactNode
  className?: string
  minChildWidth?: '12' | '16' | '20' | '24' | '28' | '32' | '36' | '40' | '44' | '48' | '56' | '64' | '72' | '80'
  gap?: '0' | '1' | '2' | '3' | '4' | '5' | '6' | '8' | '10' | '12' | '16'
}

export function AutoFitGrid({
  children,
  className = '',
  minChildWidth = '48',
  gap = '6'
}: AutoFitGridProps) {
  const minChildWidthClass = `min-${minChildWidth}`
  const gapClass = `gap-${gap}`

  return (
    <div
      className={`grid grid-cols-[repeat(auto-fit,minmax(min(${minChildWidthClass},100%),1fr))] ${gapClass} ${className}`}
      style={{
        gridTemplateColumns: `repeat(auto-fit, minmax(min(${minChildWidth}px, 100%), 1fr))`
      }}
    >
      {children}
    </div>
  )
}