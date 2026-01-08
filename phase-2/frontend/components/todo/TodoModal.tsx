import { TaskForm, TaskFormValues } from './task-form';
import { Modal } from '../ui/modal';

interface TodoModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (values: TaskFormValues) => Promise<void>;
  todo?: any;
}

export const TodoModal = ({ isOpen, onClose, onSave, todo }: TodoModalProps) => {
  const handleSubmit = async (values: TaskFormValues) => {
    await onSave(values);
  };

  const initialData = todo ? {
    title: todo.title,
    description: todo.description || '',
    priority: todo.priority || 'medium',
    dueDate: todo.due_date || ''
  } : undefined;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={todo ? "Edit Todo" : "Create New Todo"}>
      <TaskForm
        initialValues={initialData}
        onSubmit={handleSubmit}
        onCancel={onClose}
        submitText={todo ? "Update Todo" : "Create Todo"}
      />
    </Modal>
  );
};