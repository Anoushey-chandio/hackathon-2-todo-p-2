import Link from 'next/link';

export default function WelcomePage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-6 bg-white dark:bg-black text-black dark:text-white text-center">
      <h1 className="text-4xl font-bold mb-4 text-light-purple">Welcome!</h1>
      <p className="text-xl mb-8">The easiest way to manage your tasks</p>
      
      {/* Placeholder for cartoon illustration */}
      <div className="w-64 h-64 bg-light-cyan rounded-full flex items-center justify-center mb-8 opacity-50">
        <span className="text-gray-700">Illustration Placeholder</span>
      </div>

      <div className="flex gap-4">
        <Link href="/tasks" className="px-6 py-3 bg-light-purple text-white rounded hover:bg-opacity-90">
          Go to Tasks
        </Link>
      </div>
    </div>
  );
}