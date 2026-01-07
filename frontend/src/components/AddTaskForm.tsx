'use client';

import { useState } from 'react';
import { createTask } from '@/lib/api_tasks';

interface AddTaskFormProps {
  onTaskAdded: () => void;
}

export default function AddTaskForm({ onTaskAdded }: AddTaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);
    try {
      await createTask(title, description);
      setTitle('');
      setDescription('');
      onTaskAdded();
    } catch (error) {
      console.error(error);
      alert('Failed to add task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6 p-4 bg-white dark:bg-gray-800 rounded shadow-md border border-gray-200 dark:border-gray-700">
      <h2 className="text-xl font-semibold mb-4 text-light-purple">Add New Task</h2>
      <div className="flex flex-col gap-3">
        <input
          type="text"
          placeholder="Task Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="p-2 border rounded border-gray-300 dark:border-gray-600 dark:bg-gray-700"
          required
        />
        <textarea
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="p-2 border rounded border-gray-300 dark:border-gray-600 dark:bg-gray-700"
        />
        <button 
          type="submit" 
          disabled={loading}
          className="p-2 bg-light-purple text-white rounded hover:bg-opacity-90 disabled:opacity-50"
        >
          {loading ? 'Adding...' : 'Add Task'}
        </button>
      </div>
    </form>
  );
}
