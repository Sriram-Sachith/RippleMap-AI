import type { Metadata } from 'next';
import '../styles/globals.css';
import { Navbar } from '@/components/Navigation/Navbar';
import { Footer } from '@/components/Navigation/Footer';
import { QueryProvider } from '@/components/Providers/QueryProvider';

export const metadata: Metadata = {
  title: 'RippleMap AI - Geospatial Intelligence Platform',
  description: 'See the impact. Find the vulnerable. Plan the response. RippleMap AI helps communities understand road disruptions and essential service accessibility.',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className="bg-gray-50 text-gray-900">
        <QueryProvider>
          <div className="flex flex-col min-h-screen">
            <Navbar />
            <main className="flex-1">
              {children}
            </main>
            <Footer />
          </div>
        </QueryProvider>
      </body>
    </html>
  );
}
