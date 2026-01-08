'use client';

import { useEffect, useState } from 'react';
import { getTasks, Task } from '@/lib/api_tasks';
import AddTaskForm from '@/components/AddTaskForm';
import TaskList from '@/components/TaskList';
import { useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth-client';
import Image from 'next/image';

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
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleLogout = async () => {
      await authClient.signOut();
      router.push('/login');
  };

  return (
    <div className="min-h-screen p-6 bg-white dark:bg-black text-black dark:text-white">
      <div className="max-w-4xl mx-auto">
        <header className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-light-purple">My Tasks</h1>
          <button 
            onClick={handleLogout}
            className="text-sm px-4 py-2 border rounded hover:bg-gray-100 dark:hover:bg-gray-800"
          >
            Logout
          </button>
        </header>

        <div className="grid md:grid-cols-3 gap-8">
            <div className="md:col-span-1">
                 <AddTaskForm onTaskAdded={fetchTasks} />
            </div>
            <div className="md:col-span-2">
                {loading ? (
                  <p className="text-center py-8">Loading tasks...</p>
                ) : tasks.length === 0 ? (
                  <div className="flex flex-col items-center justify-center p-8 text-center text-gray-500">
                      <Image src="/assets/tasks-illustration.svg" alt="No Tasks" width={200} height={200} className="mb-4" />
                      <p>You're all caught up! Add a new task to get started.</p>
                  </div>
                ) : (
                  <TaskList tasks={tasks} onTaskUpdated={fetchTasks} />
                )}
            </div>
        </div>
      </div>
    </div>
  );
}
