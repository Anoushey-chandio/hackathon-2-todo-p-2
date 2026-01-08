import Image from 'next/image';

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 dark:bg-gray-900 p-4">
      <div className="flex w-full max-w-4xl bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
        <div className="hidden md:flex w-1/2 bg-light-purple items-center justify-center p-8">
          <Image 
            src="/assets/auth-illustration.svg" 
            alt="Authentication" 
            width={300} 
            height={300} 
            className="object-contain"
          />
        </div>
        <div className="w-full md:w-1/2 p-8 flex items-center justify-center">
          <div className="w-full max-w-md">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}
