'use client';

import { useState } from 'react';
import { taskApi, Task } from '@/lib/api_tasks';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: () => void;
}

export default function TaskList({ tasks, onTaskUpdated }: TaskListProps) {
  const [editingId, setEditingId] = useState<number | null>(null);
  const [title, setTitle] = useState('');

  const toggleComplete = async (task: Task) => {
    await taskApi.update(task.id, {
      is_completed: !task.is_completed,
    });
    onTaskUpdated();
  };

  const startEdit = (task: Task) => {
    setEditingId(task.id);
    setTitle(task.title);
  };

  const saveEdit = async (id: number) => {
    await taskApi.update(id, { title });
    setEditingId(null);
    onTaskUpdated();
  };

  const deleteTask = async (id: number) => {
    await taskApi.delete(id);
    onTaskUpdated();
  };

  return (
    <div className="flex flex-col gap-3">
      {tasks.map((task) => (
        <div
          key={task.id}
          className={`flex items-center justify-between p-4 rounded-xl border transition
          ${
            task.is_completed
              ? 'bg-green-50 border-green-200'
              : 'bg-white border-gray-200'
          }`}
        >
          {/* LEFT */}
          <div className="flex items-center gap-3 flex-1">
            {/* MARK COMPLETE */}
            <button
              onClick={() => toggleComplete(task)}
              className={`w-6 h-6 rounded-full border-2 flex items-center justify-center
              transition hover:scale-105
              ${
                task.is_completed
                  ? 'bg-green-500 border-green-500 text-white'
                  : 'border-gray-400 hover:border-light-purple'
              }`}
            >
              {task.is_completed && '✓'}
            </button>

            {/* TITLE / INPUT */}
            {editingId === task.id ? (
              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="
                  w-full px-3 py-1 rounded
                  border border-gray-300
                  focus:outline-none
                  focus:border-light-purple
                  focus:ring-2
                  focus:ring-light-purple/30
                  transition
                "
              />
            ) : (
              <span
                className={`font-medium transition ${
                  task.is_completed ? 'line-through text-gray-400' : ''
                }`}
              >
                {task.title}
              </span>
            )}
          </div>

          {/* BUTTONS */}
          <div className="flex gap-2 ml-4">
            {editingId === task.id ? (
              <button
                onClick={() => saveEdit(task.id)}
                className="
                  bg-green-500 text-white px-4 py-1 rounded
                  hover:bg-green-600
                  shadow-sm hover:shadow-md
                  transition-all
                "
              >
                Save
              </button>
            ) : (
              <button
                onClick={() => startEdit(task)}
                className="
                  bg-light-purple text-white px-4 py-1 rounded
                  hover:bg-purple-700
                  shadow-sm hover:shadow-md
                  transition-all
                "
              >
                Update
              </button>
            )}

            <button
              onClick={() => deleteTask(task.id)}
              className="
                bg-rose-400 text-white px-4 py-1 rounded
                hover:bg-rose-600
                shadow-sm hover:shadow-md
                transition-all
              "
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
