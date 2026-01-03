import React, { useState } from 'react';
import apiClient from '../../services/api-client';

const TaskItem = ({ task, onTaskUpdate, onTaskDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleToggleComplete = async () => {
    try {
      setLoading(true);
      const updatedTask = await apiClient.updateTask(task.id, {
        ...task,
        is_completed: !task.is_completed
      });
      onTaskUpdate(updatedTask);
    } catch (err) {
      setError(err.message || 'Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = async () => {
    try {
      setLoading(true);
      const updatedTask = await apiClient.updateTask(task.id, {
        title: editTitle,
        description: editDescription,
        is_completed: task.is_completed
      });
      onTaskUpdate(updatedTask);
      setIsEditing(false);
      setError('');
    } catch (err) {
      setError(err.message || 'Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        setLoading(true);
        await apiClient.deleteTask(task.id);
        onTaskDelete(task.id);
      } catch (err) {
        setError(err.message || 'Failed to delete task');
      } finally {
        setLoading(false);
      }
    }
  };

  if (isEditing) {
    return (
      <li className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="Task title"
            />
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="mt-2 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="Task description"
              rows="2"
            />
          </div>
          <div className="ml-4 flex space-x-2">
            <button
              onClick={handleEdit}
              disabled={loading}
              className="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              Save
            </button>
            <button
              onClick={() => {
                setIsEditing(false);
                setEditTitle(task.title);
                setEditDescription(task.description || '');
                setError('');
              }}
              className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Cancel
            </button>
          </div>
        </div>
        {error && (
          <div className="mt-2 text-sm text-red-600">{error}</div>
        )}
      </li>
    );
  }

  return (
    <li className="px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <input
            id={`completed-${task.id}`}
            name={`completed-${task.id}`}
            type="checkbox"
            checked={task.is_completed}
            onChange={handleToggleComplete}
            disabled={loading}
            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <label
            htmlFor={`completed-${task.id}`}
            className={`ml-3 block text-sm font-medium ${
              task.is_completed ? 'text-gray-500 line-through' : 'text-gray-700'
            }`}
          >
            {task.title}
          </label>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => setIsEditing(true)}
            disabled={loading}
            className="inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Edit
          </button>
          <button
            onClick={handleDelete}
            disabled={loading}
            className="inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Delete
          </button>
        </div>
      </div>
      {task.description && (
        <div className="ml-7 mt-1 text-sm text-gray-500">
          {task.description}
        </div>
      )}
      <div className="ml-7 mt-1 text-xs text-gray-400">
        Created: {new Date(task.created_at).toLocaleString()}
      </div>
      {error && (
        <div className="ml-7 mt-1 text-xs text-red-600">{error}</div>
      )}
    </li>
  );
};

export default TaskItem;