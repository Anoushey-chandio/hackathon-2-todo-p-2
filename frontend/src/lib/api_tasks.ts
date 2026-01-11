import { fetchClient } from './api';

export interface Task {
  id: number;
  title: string;
  description?: string;
  is_completed: boolean;
  created_at: string;
}

export async function getTasks() {
  const res = await fetchClient('/tasks/');
  if (!res.ok) throw new Error('Failed to fetch tasks');
  return res.json();
}

export async function createTask(title: string, description?: string) {
  const res = await fetchClient('/tasks/', {
    method: 'POST',
    body: JSON.stringify({ title, description }),
  });
  if (!res.ok) throw new Error('Failed to create task');
  return res.json();
}

export async function updateTask(id: number, data: Partial<Task>) {
  const res = await fetchClient(`/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to update task');
  return res.json();
}

export async function toggleTaskCompletion(id: number) {
  const res = await fetchClient(`/tasks/${id}/complete`, {
    method: 'PATCH',
  });
  if (!res.ok) throw new Error('Failed to toggle completion');
  return res.json();
}

export async function deleteTask(id: number) {
  const res = await fetchClient(`/tasks/${id}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Failed to delete task');
}