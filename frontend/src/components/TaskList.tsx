'use client';

import { Task, toggleTaskCompletion, deleteTask } from '@/lib/api_tasks';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: () => void;
}

export default function TaskList({ tasks, onTaskUpdated }: TaskListProps) {
  const handleToggle = async (id: number) => {
    try {
      await toggleTaskCompletion(id);
      onTaskUpdated();
    } catch (error) {
      console.error(error);
      alert('Failed to update task');
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this task?')) return;
    try {
      await deleteTask(id);
      onTaskUpdated();
    } catch (error) {
      console.error(error);
      alert('Failed to delete task');
    }
  };

  if (tasks.length === 0) {
    return <p className="text-center text-gray-500 mt-8">No tasks yet. Add one above!</p>;
  }

  return (
    <div className="flex flex-col gap-4">
      {tasks.map((task) => (
        <div 
          key={task.id} 
          className={`p-4 rounded shadow-sm border flex justify-between items-center transition-all ${
            task.is_completed 
              ? 'bg-gray-100 dark:bg-gray-900 border-gray-200 dark:border-gray-800 opacity-75' 
              : 'bg-white dark:bg-gray-800 border-light-cyan'
          }`}
        >
          <div>
            <h3 className={`font-semibold text-lg ${task.is_completed ? 'line-through text-gray-500' : ''}`}>
              {task.title}
            </h3>
            {task.description && <p className="text-sm text-gray-600 dark:text-gray-400">{task.description}</p>}
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => handleToggle(task.id)}
              className={`px-3 py-1 text-sm rounded ${
                task.is_completed 
                  ? 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200' 
                  : 'bg-green-100 text-green-700 hover:bg-green-200'
              }`}
            >
              {task.is_completed ? 'Undo' : 'Done'}
            </button>
            <button
              onClick={() => handleDelete(task.id)}
              className="px-3 py-1 text-sm rounded bg-red-100 text-red-700 hover:bg-red-200"
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
