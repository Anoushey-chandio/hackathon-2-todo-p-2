'use client';

import { useEffect, useState } from 'react';
import { getTasks, Task } from '@/lib/api_tasks';
import AddTaskForm from '@/components/AddTaskForm';
import TaskList from '@/components/TaskList';
import Image from 'next/image';
import { authClient } from '@/lib/auth-client';
import { useRouter } from 'next/navigation';

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const { data: session, isPending } = authClient.useSession();
  const router = useRouter();

  const fetchTasks = async () => {
    // Session is guaranteed by AuthGuard for this route
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
    // Only fetch if session is confirmed (though AuthGuard blocks render if not)
    if (!isPending && session) {
        fetchTasks();
    }
  }, [session, isPending]);

  // Loading state handled by AuthGuard or initial state


  return (
    <div className="p-4 md:p-6 lg:p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8 md:mb-12">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2 tracking-tight">My Tasks</h1>
          <p className="text-gray-500 dark:text-gray-400 text-lg">Manage your daily goals and track productivity.</p>
        </header>

        <div className="grid lg:grid-cols-12 gap-8 items-start">
            {/* Sidebar / Add Form */}
            <div className="lg:col-span-4 lg:sticky lg:top-24 order-2 lg:order-1">
                 <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
                    <h2 className="text-xl font-bold mb-4 text-light-purple">Add New Task</h2>
                    <AddTaskForm onTaskAdded={fetchTasks} />
                 </div>
            </div>

            {/* Main Content / List */}
            <div className="lg:col-span-8 order-1 lg:order-2">
                {loading ? (
                  <div className="flex justify-center py-20">
                      <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-light-purple"></div>
                  </div>
                ) : tasks.length === 0 ? (
                  <div className="flex flex-col items-center justify-center p-12 text-center bg-gray-50 dark:bg-gray-800/50 rounded-3xl border border-dashed border-gray-200 dark:border-gray-700">
                      <Image 
                        src="/assets/tasks-illustration.svg" 
                        alt="No Tasks" 
                        width={200} 
                        height={200} 
                        className="mb-6 opacity-80 w-auto h-auto"
                        priority 
                      />
                      <h3 className="text-xl font-bold mb-2">You're all caught up!</h3>
                      <p className="text-gray-500">Create a task to get started with your day.</p>
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
