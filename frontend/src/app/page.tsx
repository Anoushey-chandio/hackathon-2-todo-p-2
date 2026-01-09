import Link from 'next/link';
import Image from 'next/image';

export default function WelcomePage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-6 bg-white dark:bg-black text-black dark:text-white text-center">
      <h1 className="text-4xl font-bold mb-4 text-light-purple">Welcome!</h1>
      <p className="text-xl mb-8">The easiest way to manage your tasks</p>
      
      <div className="mb-8">
        <Image 
          src="/assets/tasks-illustration.svg" 
          alt="Welcome Illustration" 
          width={300} 
          height={300}
          priority
        />
      </div>

      <div className="flex gap-4">
        <Link href="/tasks" className="px-6 py-3 bg-light-purple text-white rounded-xl font-bold hover:bg-opacity-90 transition-all shadow-lg shadow-purple-100">
          Go to Tasks
        </Link>
      </div>
    </div>
  );
}