import React from 'react'
import { cn } from '@/lib/utils'

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
  variant?: 'default' | 'elevated' | 'outlined' | 'interactive'
  clickable?: boolean
  hoverEffect?: boolean
  focusable?: boolean
  ariaLabel?: string
  role?: string
}

export const Card: React.FC<CardProps> = ({
  children,
  className,
  variant = 'default',
  clickable = false,
  hoverEffect = true,
  focusable = false,
  ariaLabel,
  role = 'region',
  ...props
}) => {
  const variantClasses = {
    default: 'bg-white shadow-sm',
    elevated: 'bg-white shadow-md',
    outlined: 'bg-white border border-gray-200',
    interactive: 'bg-white shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200'
  }

  const hoverClasses = hoverEffect && variant !== 'interactive'
    ? 'hover:shadow-md transition-shadow duration-200'
    : ''

  const clickableClasses = clickable
    ? 'cursor-pointer focus:ring-2 focus:ring-indigo-500 focus:outline-none'
    : ''

  const focusableClasses = focusable && !clickable
    ? 'focus:ring-2 focus:ring-indigo-500 focus:outline-none'
    : ''

  const computedClassName = cn(
    'rounded-lg border border-gray-200',
    variantClasses[variant],
    hoverClasses,
    clickableClasses,
    focusableClasses,
    className
  )

  return (
    <div
      className={computedClassName}
      role={role}
      aria-label={ariaLabel}
      tabIndex={focusable || clickable ? 0 : undefined}
      {...props}
    >
      {children}
    </div>
  )
}

export interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
  className?: string
}

export const CardHeader: React.FC<CardHeaderProps> = ({
  children,
  className,
  ...props
}) => {
  return (
    <div
      className={cn('p-6 pb-4', className)}
      {...props}
    >
      {children}
    </div>
  )
}

export interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  children: React.ReactNode
  level?: 2 | 3 | 4 | 5
  className?: string
}

export const CardTitle: React.FC<CardTitleProps> = ({
  children,
  level = 3,
  className,
  ...props
}) => {
  const HeadingTag = `h${level}` as 'h2' | 'h3' | 'h4' | 'h5'

  return (
    <HeadingTag
      className={cn(
        'font-semibold leading-none tracking-tight',
        level === 2 ? 'text-2xl' :
        level === 3 ? 'text-xl' :
        level === 4 ? 'text-lg' : 'text-base',
        className
      )}
      {...props}
    >
      {children}
    </HeadingTag>
  )
}

export interface CardDescriptionProps extends React.HTMLAttributes<HTMLParagraphElement> {
  children: React.ReactNode
  className?: string
}

export const CardDescription: React.FC<CardDescriptionProps> = ({
  children,
  className,
  ...props
}) => {
  return (
    <p
      className={cn('text-sm text-gray-500 mt-2', className)}
      {...props}
    >
      {children}
    </p>
  )
}

export interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
  className?: string
  padded?: boolean
}

export const CardContent: React.FC<CardContentProps> = ({
  children,
  className,
  padded = true,
  ...props
}) => {
  return (
    <div
      className={cn(padded ? 'p-6 pt-0' : '', className)}
      {...props}
    >
      {children}
    </div>
  )
}

export interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
  className?: string
  padded?: boolean
}

export const CardFooter: React.FC<CardFooterProps> = ({
  children,
  className,
  padded = true,
  ...props
}) => {
  return (
    <div
      className={cn(
        padded ? 'p-6 pt-0' : '',
        'flex items-center',
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}

// Compound component that combines all card elements
export interface SimpleCardProps extends CardProps {
  title?: string
  description?: string
  footer?: React.ReactNode
  headerClassName?: string
  titleClassName?: string
  descriptionClassName?: string
  contentClassName?: string
  footerClassName?: string
}

export const SimpleCard: React.FC<SimpleCardProps> = ({
  title,
  description,
  footer,
  children,
  headerClassName,
  titleClassName,
  descriptionClassName,
  contentClassName,
  footerClassName,
  ...cardProps
}) => {
  return (
    <Card {...cardProps}>
      {(title || description) && (
        <CardHeader className={headerClassName}>
          {title && <CardTitle className={titleClassName}>{title}</CardTitle>}
          {description && (
            <CardDescription className={descriptionClassName}>
              {description}
            </CardDescription>
          )}
        </CardHeader>
      )}
      {children && <CardContent className={contentClassName}>{children}</CardContent>}
      {footer && <CardFooter className={footerClassName}>{footer}</CardFooter>}
    </Card>
  )
}

// Specialized card for interactive elements
export interface InteractiveCardProps extends CardProps {
  onClick?: () => void
  onKeyDown?: (e: React.KeyboardEvent) => void
  tabIndex?: number
}

export const InteractiveCard: React.FC<InteractiveCardProps> = ({
  onClick,
  onKeyDown,
  tabIndex = 0,
  children,
  ...props
}) => {
  const handleClick = () => {
    onClick?.()
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      onClick?.()
    }
    onKeyDown?.(e)
  }

  return (
    <Card
      clickable={!!onClick}
      focusable={true}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      tabIndex={tabIndex}
      {...props}
    >
      {children}
    </Card>
  )
}