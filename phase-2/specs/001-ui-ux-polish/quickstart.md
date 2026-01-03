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
   ```javascript
   /** @type {import('tailwindcss').Config} */
   module.exports = {
     content: [
       './src/**/*.{js,ts,jsx,tsx,mdx}',
     ],
     theme: {
       extend: {},
     },
     plugins: [],
   }
   ```

3. **Environment Configuration**
   Set up required environment variables in `.env.local`:
   ```bash
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
   ```

## Component Development

### Creating a New UI Component
1. Navigate to the appropriate directory in `frontend/src/components/`
2. Create a new component file (e.g., `button.tsx`)
3. Follow the component contract defined in `contracts/ui-contracts.md`
4. Implement all required states (idle, hover, active, disabled)
5. Add proper accessibility attributes
6. Test responsiveness across breakpoints

### Example Component Structure
```tsx
import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  className?: string;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  className = ''
}) => {
  const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';

  const variantClasses = {
    primary: disabled
      ? 'bg-gray-400 cursor-not-allowed'
      : 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500',
    secondary: disabled
      ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
      : 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
    outline: disabled
      ? 'border border-gray-300 text-gray-400 cursor-not-allowed'
      : 'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 focus:ring-blue-500'
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base'
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      onClick={onClick}
      disabled={disabled}
      aria-disabled={disabled}
    >
      {children}
    </button>
  );
};
```

## Responsive Design

### Breakpoint Usage
Use Tailwind's responsive prefixes to implement responsive design:
- Mobile-first approach: Base styles are mobile, use prefixes for larger screens
- `sm:` - Small screens (640px and up)
- `md:` - Medium screens (768px and up)
- `lg:` - Large screens (1024px and up)
- `xl:` - Extra large screens (1280px and up)

### Example Responsive Layout
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
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
Use Tailwind's color classes or extend the theme:
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
        }
      }
    }
  }
}
```

## Testing Components

1. **Unit Tests**
   ```bash
   npm run test:unit
   ```

2. **Accessibility Tests**
   ```bash
   npm run test:accessibility
   ```

3. **Responsive Tests**
   - Test components at different screen sizes
   - Use browser dev tools to simulate different devices
   - Verify touch target sizes (minimum 44px)

## Key Features

- **Component Consistency**: All components follow the same design system
- **Accessibility**: WCAG 2.1 AA compliance across all components
- **Responsive Design**: Mobile-first approach with responsive breakpoints
- **Type Safety**: Full TypeScript support for components
- **Performance**: Optimized rendering with proper React patterns
- **Maintainability**: Clear component structure and documentation

## Running the Development Server

1. Start the development server:
   ```bash
   npm run dev
   ```

2. Navigate to the components to verify UI polish:
   - Check responsive behavior on different screen sizes
   - Verify accessibility features work properly
   - Test keyboard navigation
   - Validate touch target sizes

## Testing the Implementation

1. **Visual Testing**: Compare designs across different browsers and devices
2. **Accessibility Testing**: Use tools like axe-core or WAVE to verify accessibility
3. **Responsive Testing**: Test on mobile, tablet, and desktop views
4. **Performance Testing**: Verify page load times and component rendering efficiency
5. **User Testing**: Validate with real users across different abilities and devices