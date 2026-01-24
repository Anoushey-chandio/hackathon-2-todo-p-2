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

// Helper to handle response errors
async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    if (res.status === 401) throw new Error('Unauthorized. Please login.');
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Request failed (${res.status})`);
  }
  
  if (res.status === 204) return {} as T;
  
  return res.json();
}

export const taskApi = {
  // Get all tasks with optional pagination
  getAll: async (skip: number = 0, limit: number = 100): Promise<Task[]> => {
    const res = await fetchClient('/api/tasks/', { // ✅ add /api and trailing slash
      method: 'GET',
    }, { skip, limit });

    return handleResponse<Task[]>(res);
  },

  // Create a new task
  create: async (data: CreateTaskData): Promise<Task> => {
    const res = await fetchClient('/api/tasks/', { // ✅ add /api and trailing slash
      method: 'POST',
      body: JSON.stringify(data),
    });

    return handleResponse<Task>(res);
  },

  // Update an existing task by ID
  update: async (id: number, data: UpdateTaskData): Promise<Task> => {
    const res = await fetchClient(`/api/tasks/${id}`, { // ❌ removed trailing slash
      method: 'PATCH',
      body: JSON.stringify(data),
    });

    return handleResponse<Task>(res);
  },

  // Delete a task by ID
  delete: async (id: number): Promise<void> => {
    const res = await fetchClient(`/api/tasks/${id}`, { // ❌ removed trailing slash
      method: 'DELETE',
    });

    await handleResponse<void>(res);
  },
};
