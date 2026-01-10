import type { Metadata } from "next";
import "./globals.css";
import AuthGuard from "@/components/AuthGuard";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "Todo App",
  description: "Phase II Todo Application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <Navbar />
        <AuthGuard>
          <main className="min-h-[calc(100vh-64px)]">
            {children}
          </main>
        </AuthGuard>
      </body>
    </html>
  );
}
