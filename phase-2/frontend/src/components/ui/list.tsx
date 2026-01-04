import React from 'react';
import { cn } from '../../lib/utils';

export interface ListProps extends React.HTMLAttributes<HTMLUListElement | HTMLOListElement | HTMLDListElement> {
  children: React.ReactNode;
  variant?: 'unordered' | 'ordered' | 'description';
  size?: 'sm' | 'md' | 'lg';
  spacing?: 'tight' | 'normal' | 'loose';
  className?: string;
  compact?: boolean;
}

export const List: React.FC<ListProps> = ({
  children,
  variant = 'unordered',
  size = 'md',
  spacing = 'normal',
  className,
  compact = false,
  ...props
}) => {
  const baseClasses = cn(
    'list-reset m-0 p-0',
    {
      'list-disc pl-5': variant === 'unordered',
      'list-decimal pl-5': variant === 'ordered',
      'pl-0': variant === 'description',
    },
    {
      'space-y-1': spacing === 'tight',
      'space-y-2': spacing === 'normal',
      'space-y-3': spacing === 'loose',
    },
    {
      'text-sm': size === 'sm',
      'text-base': size === 'md',
      'text-lg': size === 'lg',
    },
    {
      'divide-y divide-gray-200': compact && variant !== 'description',
    },
    className
  );

  const ListElement = variant === 'ordered' ? 'ol' : variant === 'description' ? 'dl' : 'ul';

  return (
    <ListElement className={baseClasses} {...props}>
      {children}
    </ListElement>
  );
};

export interface ListItemProps extends React.LiHTMLAttributes<HTMLLIElement> {
  children: React.ReactNode;
  className?: string;
  active?: boolean;
  disabled?: boolean;
  selected?: boolean;
  actionable?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export const ListItem: React.FC<ListItemProps> = ({
  children,
  className,
  active = false,
  disabled = false,
  selected = false,
  actionable = false,
  size = 'md',
  ...props
}) => {
  const baseClasses = cn(
    'relative py-2 px-3 rounded-md transition-colors duration-200',
    {
      'hover:bg-gray-50 cursor-pointer': actionable,
      'bg-indigo-50 border-l-4 border-indigo-500': active,
      'opacity-50 cursor-not-allowed': disabled,
      'bg-gray-100': selected && !active,
      'focus:outline-none focus:ring-2 focus:ring-indigo-500': actionable || !disabled,
      'text-sm': size === 'sm',
      'text-base': size === 'md',
      'text-lg': size === 'lg',
    },
    className
  );

  return (
    <li className={baseClasses} {...props}>
      {children}
    </li>
  );
};

export interface DescriptionTermProps extends React.HTMLAttributes<HTMLElement> {
  children: React.ReactNode;
  className?: string;
  emphasized?: boolean;
}

export const DescriptionTerm: React.FC<DescriptionTermProps> = ({
  children,
  className,
  emphasized = false,
  ...props
}) => {
  const baseClasses = cn(
    'font-semibold',
    {
      'text-gray-900': !emphasized,
      'text-indigo-700': emphasized,
    },
    className
  );

  return (
    <dt className={baseClasses} {...props}>
      {children}
    </dt>
  );
};

export interface DescriptionDetailProps extends React.HTMLAttributes<HTMLElement> {
  children: React.ReactNode;
  className?: string;
}

export const DescriptionDetail: React.FC<DescriptionDetailProps> = ({
  children,
  className,
  ...props
}) => {
  const baseClasses = cn(
    'text-gray-600 mt-1',
    className
  );

  return (
    <dd className={baseClasses} {...props}>
      {children}
    </dd>
  );
};

// Specialized list components
export interface SimpleListItem {
  id: string | number;
  content: React.ReactNode;
  onClick?: () => void;
  active?: boolean;
  disabled?: boolean;
}

export interface SimpleListProps {
  items: SimpleListItem[];
  onItemClick?: (id: string | number) => void;
  variant?: 'unordered' | 'ordered';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  compact?: boolean;
}

export const SimpleList: React.FC<SimpleListProps> = ({
  items,
  onItemClick,
  variant = 'unordered',
  size = 'md',
  className,
  compact = false,
}) => {
  return (
    <List variant={variant} size={size} compact={compact} className={className}>
      {items.map((item) => (
        <ListItem
          key={item.id}
          actionable={!!onItemClick || !!item.onClick}
          active={item.active}
          disabled={item.disabled}
          size={size}
          onClick={() => {
            if (item.onClick) {
              item.onClick();
            } else if (onItemClick) {
              onItemClick(item.id);
            }
          }}
        >
          {item.content}
        </ListItem>
      ))}
    </List>
  );
};

// Task list component
export interface TaskItem {
  id: string | number;
  title: string;
  description?: string;
  completed: boolean;
  priority?: 'low' | 'medium' | 'high';
  dueDate?: string;
  onClick?: () => void;
}

export interface TaskListProps {
  tasks: TaskItem[];
  onTaskClick?: (id: string | number) => void;
  className?: string;
  compact?: boolean;
}

export const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onTaskClick,
  className,
  compact = false,
}) => {
  return (
    <List variant="unordered" compact={compact} className={className}>
      {tasks.map((task) => (
        <ListItem
          key={task.id}
          actionable={!!onTaskClick}
          active={task.completed}
          onClick={() => onTaskClick && onTaskClick(task.id)}
          className={cn(
            'flex items-start',
            {
              'opacity-70': task.completed,
            }
          )}
        >
          <div className="flex items-start space-x-3">
            <input
              type="checkbox"
              checked={task.completed}
              readOnly
              className={cn(
                'h-4 w-4 mt-0.5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500',
                {
                  'bg-green-100 border-green-300': task.completed,
                }
              )}
            />
            <div className="flex-1 min-w-0">
              <div className="flex items-baseline justify-between">
                <p
                  className={cn(
                    'text-sm font-medium truncate',
                    {
                      'text-gray-900 line-through': task.completed,
                      'text-gray-700': !task.completed,
                    }
                  )}
                >
                  {task.title}
                </p>
                {task.priority && (
                  <span
                    className={cn(
                      'ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      {
                        'bg-blue-100 text-blue-800': task.priority === 'low',
                        'bg-yellow-100 text-yellow-800': task.priority === 'medium',
                        'bg-red-100 text-red-800': task.priority === 'high',
                      }
                    )}
                  >
                    {task.priority}
                  </span>
                )}
              </div>
              {task.description && (
                <p
                  className={cn(
                    'mt-1 text-sm truncate',
                    {
                      'text-gray-500': !task.completed,
                      'text-gray-400': task.completed,
                    }
                  )}
                >
                  {task.description}
                </p>
              )}
              {task.dueDate && (
                <p className="mt-1 text-xs text-gray-500">
                  Due: {new Date(task.dueDate).toLocaleDateString()}
                </p>
              )}
            </div>
          </div>
        </ListItem>
      ))}
    </List>
  );
};

// Navigation list component
export interface NavItem {
  id: string | number;
  label: string;
  href?: string;
  icon?: React.ReactNode;
  badge?: string | number;
  active?: boolean;
  disabled?: boolean;
  onClick?: () => void;
}

export interface NavListProps {
  items: NavItem[];
  onItemClick?: (id: string | number) => void;
  className?: string;
  compact?: boolean;
}

export const NavList: React.FC<NavListProps> = ({
  items,
  onItemClick,
  className,
  compact = false,
}) => {
  return (
    <List variant="unordered" compact={compact} className={className}>
      {items.map((item) => (
        <ListItem
          key={item.id}
          actionable={!item.disabled}
          active={item.active}
          disabled={item.disabled}
          onClick={() => {
            if (item.onClick) {
              item.onClick();
            } else if (onItemClick) {
              onItemClick(item.id);
            }
          }}
          className={cn(
            'flex items-center justify-between',
            {
              'bg-gray-50': item.active && !item.disabled,
            }
          )}
        >
          <div className="flex items-center space-x-3">
            {item.icon && <span className="flex-shrink-0">{item.icon}</span>}
            <span className="block truncate">{item.label}</span>
          </div>
          {item.badge && (
            <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
              {item.badge}
            </span>
          )}
        </ListItem>
      ))}
    </List>
  );
};

// Export compound component for convenience
export const ListGroup = {
  List,
  ListItem,
  DescriptionTerm,
  DescriptionDetail,
  SimpleList,
  TaskList,
  NavList,
};