import { TaskItem } from './task-item';

interface TodoCardProps {
  todo: any;
  onEdit: (todo: any) => void;
  onDelete: (id: string) => void;
  onUpdate: (id: string, data: any) => Promise<void>;
}

export const TodoCard = ({ todo, onEdit, onDelete, onUpdate }: TodoCardProps) => {
  const handleToggle = async () => {
    await onUpdate(todo.id, { ...todo, completed: !todo.completed });
  };

  return (
    <TaskItem
      id={todo.id}
      title={todo.title}
      description={todo.description}
      completed={todo.completed}
      created_at={todo.created_at}
      updated_at={todo.updated_at}
      priority={todo.priority}
      due_date={todo.due_date}
      onToggle={handleToggle}
      onEdit={() => onEdit(todo)}
      onDelete={() => onDelete(todo.id)}
    />
  );
};