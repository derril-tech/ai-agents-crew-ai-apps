import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import '@/styles/globals.css'
import { Toaster } from 'react-hot-toast'
import { Header } from '@/components/layout/Header'
import { Sidebar } from '@/components/layout/Sidebar'
import { Footer } from '@/components/layout/Footer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'SDR Assistant - AI-Powered Sales Development',
  description: 'Revolutionize your sales development with AI-powered lead analysis and email generation',
  keywords: ['SDR', 'Sales', 'AI', 'Lead Generation', 'Email Automation'],

  openGraph: {
    title: 'SDR Assistant - AI-Powered Sales Development',
    description: 'Revolutionize your sales development with AI-powered lead analysis and email generation',
    type: 'website',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'SDR Assistant',
    description: 'AI-powered sales development platform',
  },
  robots: {
    index: false, // Set to true when ready for production
    follow: false,
  },
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} h-full bg-gray-50 dark:bg-gray-900`}>
        <div className="flex h-full">
          {/* Sidebar */}
          <Sidebar />
          
                     {/* Main content area */}
           <div className="flex-1 flex flex-col overflow-hidden">
             {/* Header */}
             <Header />
             
             {/* Page content */}
             <main className="flex-1 overflow-auto bg-white dark:bg-gray-800">
               <div className="container mx-auto px-4 py-6 max-w-7xl">
                 {children}
               </div>
             </main>
             
             {/* Footer */}
             <Footer />
           </div>
        </div>
        
        {/* Toast notifications */}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#10B981',
                secondary: '#fff',
              },
            },
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#EF4444',
                secondary: '#fff',
              },
            },
          }}
        />
        
        {/* Global loading indicator */}
        <div id="global-loading" className="hidden">
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 flex items-center space-x-3">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
              <span className="text-gray-900 font-medium">Processing...</span>
            </div>
          </div>
        </div>
      </body>
    </html>
  )
}