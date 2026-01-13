# Quickstart: UI & UX Polish

## Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install next react react-dom typescript @types/react @types/node @types/react-dom
   npm install tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

2. **Configure Tailwind CSS**
   Update `tailwind.config.js`:
   ```js
   /** @type {import('tailwindcss').Config} */
   module.exports = {
     content: [
       './src/**/*.{js,ts,jsx,tsx,mdx}',
     ],
     theme: {
       extend: {
         colors: {
           primary: {
             50: '#eff6ff',
             100: '#dbeafe',
             200: '#bfdbfe',
             300: '#93c5fd',
             400: '#60a5fa',
             500: '#3b82f6',
             600: '#2563eb',
             700: '#1d4ed8',
             800: '#1e40af',
             900: '#1e3a8a',
           },
           secondary: {
             50: '#f8fafc',
             100: '#f1f5f9',
             200: '#e2e8f0',
             300: '#cbd5e1',
             400: '#94a3b8',
             500: '#64748b',
             600: '#475569',
             700: '#334155',
             800: '#1e293b',
             900: '#0f172a',
           },
           success: {
             50: '#f0fdf4',
             100: '#dcfce7',
             200: '#bbf7d0',
             300: '#86efac',
             400: '#4ade80',
             500: '#22c55e',
             600: '#16a34a',
             700: '#15803d',
             800: '#166534',
             900: '#14532d',
           },
           warning: {
             50: '#fffbeb',
             100: '#fef3c7',
             200: '#fde68a',
             300: '#fcd34d',
             400: '#fbbf24',
             500: '#f59e0b',
             600: '#d97706',
             700: '#b45309',
             800: '#92400e',
             900: '#78350f',
           },
           danger: {
             50: '#fef2f2',
             100: '#fee2e2',
             200: '#fecaca',
             300: '#fca5a5',
             400: '#f87171',
             500: '#ef4444',
             600: '#dc2626',
             700: '#b91c1c',
             800: '#991b1b',
             900: '#7f1d1d',
           },
         },
         spacing: {
           '0-5': '0.125rem',  // 2px
           '1-5': '0.375rem',  // 6px
           '2-5': '0.625rem',  // 10px
           '3-5': '0.875rem',  // 14px
         },
         borderRadius: {
           sm: '0.125rem',   // 2px
           md: '0.375rem',   // 6px
           lg: '0.5rem',     // 8px
           xl: '0.75rem',    // 12px
           '2xl': '1rem',    // 16px
           '3xl': '1.5rem',  // 24px
         },
         boxShadow: {
           xs: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
           sm: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)',
           md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)',
           lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.1)',
           xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)',
           '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
         },
       },
     },
     plugins: [],
   }
   ```

3. **Import Styles**
   In `src/app/globals.css`:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;

   /* Import theme styles */
   @import './styles/theme.css';
   @import './styles/typography.css';
   @import './styles/spacing.css';
   @import './styles/animations.css';
   @import './styles/elevation.css';
   ```

## Component Development

### Creating a New UI Component
1. Navigate to `frontend/src/components/ui/`
2. Create a new component file (e.g., `alert.tsx`)
3. Follow the existing component patterns with proper TypeScript interfaces
4. Implement all required states (idle, hover, active, disabled)
5. Add proper accessibility attributes (ARIA labels, roles, etc.)
6. Test component with keyboard navigation and screen readers

### Example Component Structure
```tsx
import React from 'react';
import { cn } from '../../lib/utils';

export interface ComponentProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  variant?: 'default' | 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const Component: React.FC<ComponentProps> = ({
  children,
  variant = 'default',
  size = 'md',
  className,
  ...props
}) => {
  const baseClasses = cn(
    'base-component-classes',
    {
      'variant-specific-classes': variant === 'variant-name',
      'size-specific-classes': size === 'size-name',
    },
    className
  );

  return (
    <div className={baseClasses} {...props}>
      {children}
    </div>
  );
};
```

## Responsive Design Implementation

### Breakpoint Usage
Use Tailwind's responsive prefixes to implement responsive design:
- Mobile-first approach: Base styles are mobile, use prefixes for larger screens
- `sm:` - Small screens (640px and up)
- `md:` - Medium screens (768px and up)
- `lg:` - Large screens (1024px and up)
- `xl:` - Extra large screens (1280px and up)
- `2xl:` - 2x extra large screens (1536px and up)

### Example Responsive Layout
```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
  <div className="p-4 bg-white rounded-lg shadow">Card 1</div>
  <div className="p-4 bg-white rounded-lg shadow">Card 2</div>
  <div className="p-4 bg-white rounded-lg shadow">Card 3</div>
</div>
```

## Accessibility Implementation

### Focus Management
- All interactive elements must be keyboard accessible
- Use `tabIndex` appropriately (avoid `tabIndex > 0`)
- Implement visible focus indicators
- Test with keyboard navigation only

### ARIA Attributes
- Use semantic HTML elements when possible
- Add ARIA labels for screen readers
- Implement ARIA roles for complex components
- Use ARIA live regions for dynamic content updates

## Theming

### Color Palette Implementation
Use the color classes from the defined palette:
- Primary colors: `text-primary-500`, `bg-primary-100`, `border-primary-300`
- Secondary colors: `text-secondary-500`, `bg-secondary-100`
- Status colors: `text-success-500`, `text-warning-500`, `text-danger-500`
- Neutral colors: `text-neutral-500`, `bg-neutral-100`

### Typography Scale
Use the defined typography classes:
- Text sizes: `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, etc.
- Font weights: `font-thin`, `font-light`, `font-normal`, `font-medium`, `font-semibold`, `font-bold`
- Line heights: `leading-none`, `leading-tight`, `leading-snug`, `leading-normal`, etc.
- Letter spacing: `tracking-tight`, `tracking-normal`, `tracking-wide`, etc.

## Spacing System

### Spacing Scale Usage
Use the consistent spacing scale:
- `p-1`, `p-2`, `p-3`, `p-4`, etc. for padding
- `m-1`, `m-2`, `m-3`, `m-4`, etc. for margins
- `gap-1`, `gap-2`, `gap-3`, `gap-4`, etc. for flexbox/grid gaps
- Directional classes: `pt-4`, `pb-2`, `ml-6`, `mr-3`, etc.

## Animation and Transitions

### Consistent Animations
Use the predefined transition classes:
- `transition`: Applies transition to all properties
- `transition-colors`: Applies transition to color-related properties
- `transition-opacity`: Applies transition to opacity
- `transition-shadow`: Applies transition to box-shadow
- `transition-transform`: Applies transition to transform

### Duration Classes
- `duration-75`: 75ms
- `duration-100`: 100ms
- `duration-150`: 150ms
- `duration-200`: 200ms
- `duration-300`: 300ms
- `duration-500`: 500ms
- `duration-700`: 700ms
- `duration-1000`: 1000ms

## Component States

### Visual Feedback States
All interactive components should implement:
- Idle: Default appearance
- Hover: Visual change when mouse hovers (if applicable)
- Focus: Visible focus indicator for keyboard navigation
- Active: Appearance when activated (clicked/held)
- Disabled: Visual indication when not interactive
- Loading: Special state for asynchronous operations

## Testing Components

1. **Visual Consistency Testing**
   ```bash
   npm run test:visual
   ```

2. **Accessibility Testing**
   - Test with keyboard navigation (Tab, Enter, Space, Arrow keys)
   - Verify ARIA attributes are properly implemented
   - Use accessibility tools like axe-core or WAVE

3. **Responsive Testing**
   - Test on different screen sizes (mobile, tablet, desktop)
   - Use browser dev tools to simulate different devices
   - Verify touch target sizes (minimum 44px)

4. **Cross-Browser Testing**
   - Test in Chrome, Firefox, Safari, and Edge
   - Verify consistent appearance and functionality

## Key Features

- **Component Consistency**: All components follow the same design system
- **Accessibility Compliance**: WCAG 2.1 AA compliance across all components
- **Responsive Design**: Mobile-first approach with responsive breakpoints
- **Type Safety**: Full TypeScript support for components
- **Performance Optimization**: Efficient rendering with proper component memoization
- **Maintainability**: Clear component structure and documentation

## Running the Development Server

1. Start the development server:
   ```bash
   npm run dev
   ```

2. Navigate to the UI components to verify visual consistency:
   - Check responsive behavior on different screen sizes
   - Verify accessibility features work properly
   - Test keyboard navigation
   - Validate visual feedback states

## Integration Testing

1. **Component Integration**
   - Verify components work together harmoniously
   - Test composition of multiple components
   - Ensure consistent styling across component combinations

2. **Visual Regression Testing**
   - Compare components against design specifications
   - Verify consistent spacing, typography, and color usage
   - Check for visual regressions in component states