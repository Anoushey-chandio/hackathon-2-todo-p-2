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
    return null; // Handled by parent
  }

  return (
    <div className="flex flex-col gap-4">
      {tasks.map((task) => (
        <div 
          key={task.id} 
          className={`group p-5 rounded-2xl border transition-all duration-200 flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center ${
            task.is_completed 
              ? 'bg-gray-50 dark:bg-gray-800/50 border-gray-100 dark:border-gray-800 opacity-75' 
              : 'bg-white dark:bg-gray-800 border-gray-100 dark:border-gray-700 hover:border-light-purple/30 hover:shadow-md'
          }`}
        >
          <div className="flex-1">
            <h3 className={`font-bold text-lg mb-1 transition-colors ${
              task.is_completed 
                ? 'line-through text-gray-400 dark:text-gray-500' 
                : 'text-gray-800 dark:text-gray-100'
            }`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`text-sm ${
                task.is_completed 
                  ? 'text-gray-400 dark:text-gray-600' 
                  : 'text-gray-500 dark:text-gray-400'
              }`}>
                {task.description}
              </p>
            )}
          </div>
          
          <div className="flex items-center gap-2 w-full sm:w-auto mt-2 sm:mt-0">
            <button
              onClick={() => handleToggle(task.id)}
              className={`flex-1 sm:flex-none px-4 py-2 text-sm font-bold rounded-xl transition-all ${
                task.is_completed 
                  ? 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600' 
                  : 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 hover:bg-green-100 dark:hover:bg-green-900/40 border border-green-100 dark:border-green-800'
              }`}
            >
              {task.is_completed ? 'Undo' : 'Complete'}
            </button>
            <button
              onClick={() => handleDelete(task.id)}
              className="flex-1 sm:flex-none px-4 py-2 text-sm font-bold rounded-xl bg-red-50 dark:bg-red-900/20 text-red-500 hover:bg-red-100 dark:hover:bg-red-900/40 border border-red-100 dark:border-red-800 transition-all opacity-0 group-hover:opacity-100 focus:opacity-100"
              title="Delete Task"
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
