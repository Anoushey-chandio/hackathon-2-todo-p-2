'use client';

import { useState } from 'react';
import { taskApi, Task } from '@/lib/api_tasks';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: () => void;
}

export default function TaskList({ tasks, onTaskUpdated }: TaskListProps) {
  const [updatingId, setUpdatingId] = useState<number | null>(null);

  const handleToggle = async (task: Task) => {
    setUpdatingId(task.id);
    try {
      await taskApi.update(task.id, { is_completed: !task.is_completed });
      onTaskUpdated();
    } catch (error) {
      console.error('Failed to update task:', error);
    } finally {
      setUpdatingId(null);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this task?')) return;
    setUpdatingId(id);
    try {
      await taskApi.delete(id);
      onTaskUpdated();
    } catch (error) {
      console.error('Failed to delete task:', error);
    } finally {
      setUpdatingId(null);
    }
  };

  if (tasks.length === 0) {
    return (
      <div className="text-center py-10 text-gray-500">
        No tasks yet. Add one above!
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3 w-full">
      {tasks.map((task) => (
        <div
          key={task.id}
          className={`flex items-center justify-between p-4 bg-white dark:bg-gray-800 rounded-xl border-2 transition-all ${
            task.is_completed
              ? 'border-green-100 dark:border-green-900 bg-green-50 dark:bg-green-900/20'
              : 'border-gray-100 dark:border-gray-700'
          }`}
        >
          <div className="flex items-center gap-3">
            <button
              onClick={() => handleToggle(task)}
              disabled={updatingId === task.id}
              className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${
                task.is_completed
                  ? 'bg-green-500 border-green-500 text-white'
                  : 'border-gray-300 hover:border-light-purple'
              }`}
            >
              {task.is_completed && '✓'}
            </button>
            <span
              className={`font-medium ${
                task.is_completed ? 'text-gray-400 line-through' : ''
              }`}
            >
              {task.title}
            </span>
          </div>
          <button
            onClick={() => handleDelete(task.id)}
            disabled={updatingId === task.id}
            className="text-gray-400 hover:text-red-500 transition-colors px-2"
          >
            Delete
          </button>
        </div>
      ))}
    </div>
  );
}