'use client';

import { useEffect, useState } from 'react';
import { getTasks, Task } from '@/lib/api_tasks';
import AddTaskForm from '@/components/AddTaskForm';
import TaskList from '@/components/TaskList';
import { useRouter } from 'next/navigation';

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const fetchTasks = async () => {
    try {
      const data = await getTasks();
      setTasks(data);
    } catch (error) {
      console.error(error);
      // If error (401 handled by fetchClient), maybe just stop loading
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div className="min-h-screen p-6 bg-white dark:bg-black text-black dark:text-white">
      <div className="max-w-2xl mx-auto">
        <header className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-light-purple">My Tasks</h1>
          <button 
            onClick={() => {
              document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
              localStorage.removeItem('token');
              router.push('/login');
            }}
            className="text-sm text-gray-500 hover:text-black dark:hover:text-white"
          >
            Logout
          </button>
        </header>

        <AddTaskForm onTaskAdded={fetchTasks} />
        
        {loading ? (
          <p className="text-center py-8">Loading tasks...</p>
        ) : (
          <TaskList tasks={tasks} onTaskUpdated={fetchTasks} />
        )}
      </div>
    </div>
  );
}
