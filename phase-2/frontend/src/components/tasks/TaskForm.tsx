import React, { useState } from 'react';
import { taskService } from '@/services/task';

interface TaskFormValues {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
}

interface TaskFormProps {
  onTaskCreated?: (task: any) => void;
  initialValues?: Partial<TaskFormValues>;
}

const TaskForm: React.FC<TaskFormProps> = ({ onTaskCreated, initialValues = {} }) => {
  const [title, setTitle] = useState(initialValues.title || '');
  const [description, setDescription] = useState(initialValues.description || '');
  const [priority, setPriority] = useState< 'low' | 'medium' | 'high'>(initialValues.priority || 'medium');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    try {
      setLoading(true);
      const newTask = await taskService.createTask({
        title: title.trim(),
        description: description.trim() || undefined,
        completed: false,
        priority: priority,
      });
      setTitle('');
      setDescription('');
      setPriority('medium');
      setError('');
      if (onTaskCreated) {
        onTaskCreated(newTask);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white shadow sm:rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900">Create a new task</h3>
        <div className="mt-2 max-w-xl text-sm text-gray-500">
          <p>Add a new task to your list.</p>
        </div>
        <form onSubmit={handleSubmit} className="mt-5 space-y-4">
          <div className="w-full">
            <label htmlFor="task-title" className="block text-sm font-medium text-gray-700 mb-1">
              Task Title *
            </label>
            <input
              type="text"
              name="task-title"
              id="task-title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="What needs to be done?"
              className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
              disabled={loading}
            />
          </div>

          <div className="w-full">
            <label htmlFor="task-description" className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              id="task-description"
              name="task-description"
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 mt-1 block w-full sm:text-sm border border-gray-300 rounded-md p-2"
              placeholder="Add details about this task..."
              disabled={loading}
            />
          </div>

          <div className="w-full">
            <label htmlFor="task-priority" className="block text-sm font-medium text-gray-700 mb-1">
              Priority
            </label>
            <select
              id="task-priority"
              name="task-priority"
              value={priority}
              onChange={(e) => setPriority(e.target.value as 'low' | 'medium' | 'high')}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
              disabled={loading}
            >
              <option value="low">Low Priority</option>
              <option value="medium">Medium Priority</option>
              <option value="high">High Priority</option>
            </select>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {loading ? 'Creating...' : 'Add Task'}
            </button>
          </div>
        </form>
        {error && (
          <div className="mt-2 text-sm text-red-600">{error}</div>
        )}
      </div>
    </div>
  );
};

export default TaskForm;