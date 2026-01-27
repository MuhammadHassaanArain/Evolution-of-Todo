import { apiClient } from '../lib/api/client';

export interface Task {
  id: string | number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string; // backend format
  updated_at: string; // backend format
  priority?: 'low' | 'medium' | 'high';
  due_date?: string; // backend format
}

// Transform backend format to frontend format
const transformTaskFromBackend = (backendTask: any): Task => {
  return {
    id: backendTask.id,
    title: backendTask.title,
    description: backendTask.description || undefined,
    completed: backendTask.completed || false,
    created_at: backendTask.created_at || backendTask.createdAt,
    updated_at: backendTask.updated_at || backendTask.updatedAt,
    priority: backendTask.priority || 'medium',
    due_date: backendTask.due_date || backendTask.dueDate || undefined,
  };
};

// Transform frontend format to backend format
const transformTaskToBackend = (frontendTask: Partial<Task>): any => {
  return {
    title: frontendTask.title,
    description: frontendTask.description || null,
    completed: frontendTask.completed,
    priority: frontendTask.priority || 'medium',
    due_date: frontendTask.due_date || null,
  };
};

export const taskService = {
  // Get all public tasks
  async getTasks(): Promise<Task[]> {
    try {
      const response = await apiClient.get<any>('/tasks', { requiresAuth: false });
      // Handle different possible response formats from backend
      const tasksData = Array.isArray(response) ? response : response.tasks || response.data || [];
      return tasksData.map(transformTaskFromBackend);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  },

  // Get a single task by ID
  async getTask(id: string | number): Promise<Task> {
    try {
      const response = await apiClient.get<any>(`/tasks/${id}`, { requiresAuth: false });
      return transformTaskFromBackend(response);
    } catch (error) {
      console.error(`Error fetching task ${id}:`, error);
      throw error;
    }
  },

  // Create a new task
  async createTask(taskData: Partial<Task>): Promise<Task> {
    try {
      const backendData = transformTaskToBackend(taskData);
      const response = await apiClient.post<any>('/tasks', backendData, { requiresAuth: false });
      return transformTaskFromBackend(response);
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  },

  // Update an existing task
  async updateTask(id: string | number, taskData: Partial<Task>): Promise<Task> {
    try {
      const backendData = transformTaskToBackend(taskData);
      const response = await apiClient.put<any>(`/tasks/${id}`, backendData, { requiresAuth: false });
      return transformTaskFromBackend(response);
    } catch (error) {
      console.error(`Error updating task ${id}:`, error);
      throw error;
    }
  },

  // Delete a task
  async deleteTask(id: string | number): Promise<void> {
    try {
      await apiClient.delete<any>(`/tasks/${id}`, { requiresAuth: false });
    } catch (error) {
      console.error(`Error deleting task ${id}:`, error);
      throw error;
    }
  },

  // Toggle task completion status
  async toggleTaskCompletion(id: string | number): Promise<Task> {
    try {
      const currentTask = await this.getTask(id);
      const updatedTask = await this.updateTask(id, {
        ...currentTask,
        completed: !currentTask.completed,
      });
      return updatedTask;
    } catch (error) {
      console.error(`Error toggling task completion ${id}:`, error);
      throw error;
    }
  },
};