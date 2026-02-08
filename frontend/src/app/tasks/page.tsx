'use client';

import { useEffect, useState, useCallback } from 'react';
import { useSession } from '@/lib/session';
import { taskApi, Task } from '@/lib/api_tasks';
import AddTaskForm from '@/components/AddTaskForm';
import TaskList from '@/components/TaskList';
import ChatWidget from '@/components/Chat/ChatWidget';

export default function TasksPage() {
  const { user, isLoading: sessionLoading } = useSession();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = useCallback(async (silent = false) => {
    if (!silent) setLoading(true);
    setError(null);
    try {
      const data = await taskApi.getAll();
      setTasks(data);
    } catch (err: any) {
      console.error('Error fetching tasks:', err);
      setError('Error fetching tasks. Please try again.');
    } finally {
      if (!silent) setLoading(false);
    }
  }, []);

  // ✅ Sirf data fetch karein, redirection AuthGuard sambhaal lega
  useEffect(() => {
    if (!sessionLoading && user) {
      fetchTasks();
    }
  }, [sessionLoading, user, fetchTasks]);

  if (sessionLoading) return null;

  return (
    <div className="p-4 md:p-6 lg:p-8 min-h-screen">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8 md:mb-12">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2 tracking-tight">
            My Tasks
          </h1>
          <p className="text-gray-500 dark:text-gray-400 text-lg">
            Manage your daily goals and track productivity.
          </p>
        </header>

        {loading && tasks.length === 0 ? (
          <div className="flex justify-center py-20">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-purple-500"></div>
          </div>
        ) : error ? (
          <div className="p-4 text-center text-red-500">{error}</div>
        ) : (
          <div className="grid lg:grid-cols-12 gap-8 items-start">
            <div className="lg:col-span-4 lg:sticky lg:top-24 order-2 lg:order-1">
              <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
                <h2 className="text-xl font-bold mb-4 text-purple-600">
                  Add New Task
                </h2>
                <AddTaskForm onTaskAdded={() => fetchTasks(true)} />
              </div>
            </div>

            <div className="lg:col-span-8 order-1 lg:order-2">
              {tasks.length === 0 ? (
                <div className="flex flex-col items-center justify-center p-12 text-center bg-gray-50 dark:bg-gray-800/50 rounded-3xl border border-dashed border-gray-200 dark:border-gray-700">
                  <h3 className="text-xl font-bold mb-2">You're all caught up!</h3>
                  <p className="text-gray-500">Create a task to get started.</p>
                </div>
              ) : (
                <TaskList tasks={tasks} onTaskUpdated={() => fetchTasks(true)} />
              )}
            </div>
          </div>
        )}
      </div>
      <ChatWidget onTaskAdded={() => fetchTasks(true)} />
    </div>
  );
}