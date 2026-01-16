import { fetchClient } from './api';

export interface Task {
  id: number;
  title: string;
  description?: string;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskData {
  title: string;
  description?: string;
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

export const taskApi = {
  getAll: async (): Promise<Task[]> => {
    const res = await fetchClient('api/tasks/');
    if (!res.ok) throw new Error('Failed to fetch tasks');
    return res.json();
  },

  create: async (data: CreateTaskData): Promise<Task> => {
    const res = await fetchClient('api/tasks/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to create task');
    return res.json();
  },

  update: async (id: number, data: UpdateTaskData): Promise<Task> => {
    const res = await fetchClient(`api/tasks/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to update task');
    return res.json();
  },

  delete: async (id: number): Promise<void> => {
    const res = await fetchClient(`api/tasks/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete task');
  },
};
