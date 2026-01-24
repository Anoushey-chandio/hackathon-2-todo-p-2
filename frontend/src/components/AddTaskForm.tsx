'use client';

import { useState } from 'react';
import { taskApi, Task } from '@/lib/api_tasks';

interface AddTaskFormProps {
  onTaskAdded: () => void;
}

export default function AddTaskForm({ onTaskAdded }: AddTaskFormProps) {
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);

    try {
      // Token is automatically included by fetchClient via sessionManager
      // Check sessionManager state first
      await taskApi.create({ title });
      setTitle('');
      onTaskAdded(); // Refresh tasks after adding
    } catch (error) {
      console.error('Failed to add task:', error);
      alert('Failed to add task. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-4 w-full">
      <input
        type="text"
        placeholder="Add a new task..."
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="flex-1 p-3 border-2 rounded-xl border-gray-200 focus:border-light-purple outline-none transition-all dark:bg-gray-800 dark:border-gray-700"
        disabled={loading}
      />
      <button
        type="submit"
        disabled={loading || !title.trim()}
        className="px-6 py-3 bg-light-purple text-white font-bold rounded-xl hover:bg-purple-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? 'Adding...' : 'Add'}
      </button>
    </form>
  );
}
