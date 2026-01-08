'use client';

import { useState } from 'react';
import { TaskList } from './task-list';
import { TaskForm } from './task-form';
import { useTasks } from '../../hooks/task';
import { Task } from '../../services/task';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';

export default function TaskListContainer() {
  const {
    tasks,
    loading,
    error,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  } = useTasks();

  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [formError, setFormError] = useState<string | null>(null);

  const handleCreateTask = async (formData: any) => {
    try {
      setFormError(null);
      await createTask({
        title: formData.title,
        description: formData.description,
        priority: formData.priority,
        due_date: formData.dueDate,
        completed: false,
      });
      setEditingTask(null); // Clear any editing state
    } catch (err) {
      console.error('Failed to create task:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to create task';
      setFormError(errorMessage);
      throw err;
    }
  };

  const handleUpdateTask = async (formData: any) => {
    if (!editingTask) return;

    try {
      setFormError(null);
      await updateTask(editingTask.id, {
        title: formData.title,
        description: formData.description,
        priority: formData.priority,
        due_date: formData.dueDate,
      });
      setEditingTask(null);
    } catch (err) {
      console.error('Failed to update task:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to update task';
      setFormError(errorMessage);
      throw err;
    }
  };

  const handleEditTask = (taskId: string | number) => {
    const task = tasks.find(t => t.id === taskId);
    if (task) {
      setEditingTask(task);
    }
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
    setFormError(null);
  };

  const handleToggleTask = async (taskId: string | number) => {
    try {
      await toggleTaskCompletion(taskId);
    } catch (err) {
      console.error('Failed to toggle task:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to toggle task completion';
      setFormError(errorMessage);
    }
  };

  const handleDeleteTask = async (taskId: string | number) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(taskId);
      } catch (err) {
        console.error('Failed to delete task:', err);
        const errorMessage = err instanceof Error ? err.message : 'Failed to delete task';
        setFormError(errorMessage);
      }
    }
  };

  if (loading) {
    return (
      <Card>
        <CardContent className="p-8 text-center">
          <div className="flex flex-col items-center">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600 mb-2"></div>
            <p>Loading tasks...</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent className="p-8 text-center">
          <div className="text-red-600 mb-4">
            <p className="font-medium">Error loading tasks:</p>
            <p className="text-sm mt-1">{error}</p>
          </div>
          <div className="flex justify-center space-x-3">
            <Button
              onClick={() => window.location.reload()}
              variant="outline"
            >
              Retry
            </Button>
            <Button
              onClick={() => {
                localStorage.removeItem('access_token');
                localStorage.removeItem('token');
                window.location.href = '/login';
              }}
              variant="destructive"
            >
              Logout
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>{editingTask ? 'Edit Task' : 'Create New Task'}</CardTitle>
        </CardHeader>
        <CardContent>
          {formError && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-sm text-red-700">{formError}</p>
            </div>
          )}
          <TaskForm
            initialValues={{
              title: editingTask?.title || '',
              description: editingTask?.description || '',
              priority: editingTask?.priority || 'medium',
              dueDate: editingTask?.due_date || '',
            }}
            onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
            onCancel={editingTask ? handleCancelEdit : undefined}
            submitText={editingTask ? 'Update Task' : 'Create Task'}
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>My Tasks ({tasks.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <TaskList
            tasks={tasks}
            onToggleTask={handleToggleTask}
            onEditTask={handleEditTask}
            onDeleteTask={handleDeleteTask}
          />
        </CardContent>
      </Card>
    </div>
  );
}