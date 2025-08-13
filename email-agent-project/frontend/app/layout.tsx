// frontend/app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';
import { Toaster } from 'react-hot-toast';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Email Agent - AI-Powered Email Management',
  description: 'Intelligent email processing with AI agents',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          {children}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#1e293b',
                color: '#fff',
                border: '1px solid #334155',
              },
            }}
          />
        </Providers>
      </body>
    </html>
  );
}

// frontend/app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { ThemeProvider } from 'next-themes';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
            retry: 1,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
        {children}
      </ThemeProvider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

// frontend/app/globals.css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
  }
}

@layer components {
  .glass-effect {
    @apply bg-white/10 dark:bg-gray-900/10 backdrop-blur-lg border border-white/20 dark:border-gray-700/20;
  }

  .gradient-border {
    @apply relative;
    background: linear-gradient(to right, #3b82f6, #8b5cf6);
    padding: 1px;
  }

  .gradient-text {
    @apply bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-600;
  }

  .pulse-dot {
    @apply relative;
  }

  .pulse-dot::before {
    content: '';
    @apply absolute -inset-1 bg-green-500 rounded-full animate-ping;
  }

  .pulse-dot::after {
    content: '';
    @apply absolute inset-0 bg-green-500 rounded-full;
  }
}

@layer utilities {
  .animation-delay-200 {
    animation-delay: 200ms;
  }

  .animation-delay-400 {
    animation-delay: 400ms;
  }

  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
}

/* Custom animations */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes glow-pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-glow-pulse {
  animation: glow-pulse 2s ease-in-out infinite;
}

// frontend/app/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { 
  Mail, Bot, Sparkles, Shield, Zap, BarChart3, 
  ArrowRight, CheckCircle, Globe, Clock 
} from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
  const router = useRouter();
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  const features = [
    {
      icon: Bot,
      title: 'AI-Powered Agents',
      description: 'Four specialized agents work together to process your emails intelligently',
      color: 'from-blue-500 to-cyan-500',
    },
    {
      icon: Zap,
      title: 'Real-time Processing',
      description: 'Emails are categorized and drafted instantly with WebSocket updates',
      color: 'from-purple-500 to-pink-500',
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your data is encrypted and never shared. Full control over your emails',
      color: 'from-green-500 to-emerald-500',
    },
    {
      icon: BarChart3,
      title: 'Analytics Dashboard',
      description: 'Track performance, response times, and email patterns',
      color: 'from-orange-500 to-red-500',
    },
  ];

  const stats = [
    { label: 'Emails Processed', value: '10K+', icon: Mail },
    { label: 'Time Saved', value: '500hrs', icon: Clock },
    { label: 'Accuracy Rate', value: '95%', icon: CheckCircle },
    { label: 'Active Users', value: '100+', icon: Globe },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900">
      {/* Animated background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -inset-10 opacity-50">
          {[...Array(20)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute h-64 w-64 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 opacity-10 blur-3xl"
              animate={{
                x: [0, 100, -100, 0],
                y: [0, -100, 100, 0],
              }}
              transition={{
                duration: 10 + i * 2,
                repeat: Infinity,
                ease: 'linear',
              }}
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
              }}
            />
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="relative z-10">
        {/* Navigation */}
        <nav className="flex items-center justify-between p-6 lg:px-8">
          <div className="flex items-center space-x-2">
            <Mail className="h-8 w-8 text-blue-400" />
            <span className="text-2xl font-bold text-white">Email Agent</span>
          </div>
          <div className="flex items-center space-x-6">
            <Link
              href="/dashboard"
              className="text-white hover:text-blue-400 transition-colors"
            >
              Dashboard
            </Link>
            <button
              onClick={() => router.push('/dashboard')}
              className="px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all transform hover:scale-105"
            >
              Get Started
            </button>
          </div>
        </nav>

        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: isLoaded ? 1 : 0, y: isLoaded ? 0 : 20 }}
          transition={{ duration: 0.8 }}
          className="max-w-7xl mx-auto px-6 pt-20 pb-32 text-center"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
            className="inline-flex items-center px-4 py-2 bg-blue-500/20 rounded-full mb-8 border border-blue-500/30"
          >
            <Sparkles className="h-4 w-4 text-blue-400 mr-2" />
            <span className="text-blue-300 text-sm">Powered by GPT-4 & Gemini</span>
          </motion.div>

          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
            Your AI Email
            <span className="gradient-text"> Assistant</span>
          </h1>

          <p className="text-xl text-gray-300 mb-12 max-w-3xl mx-auto">
            Let intelligent agents handle your inbox. Categorize, prioritize, and draft responses
            automatically while you focus on what matters.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => router.push('/dashboard')}
              className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl text-lg font-semibold hover:from-blue-600 hover:to-purple-700 transition-all transform hover:scale-105 flex items-center justify-center"
            >
              Start Processing Emails
              <ArrowRight className="ml-2 h-5 w-5" />
            </button>
            <button className="px-8 py-4 bg-white/10 backdrop-blur-lg text-white rounded-xl text-lg font-semibold hover:bg-white/20 transition-all border border-white/20">
              Watch Demo
            </button>
          </div>
        </motion.div>

        {/* Stats Section */}
        <div className="max-w-7xl mx-auto px-6 pb-20">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className="glass-effect rounded-xl p-6 text-center"
              >
                <stat.icon className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                <div className="text-3xl font-bold text-white">{stat.value}</div>
                <div className="text-gray-400 text-sm">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Features Grid */}
        <div className="max-w-7xl mx-auto px-6 pb-32">
          <motion.h2
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="text-3xl font-bold text-white text-center mb-12"
          >
            Powerful Features
          </motion.h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1 + index * 0.1 }}
                whileHover={{ y: -5 }}
                className="glass-effect rounded-xl p-6 hover:border-blue-500/50 transition-all"
              >
                <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${feature.color} p-2.5 mb-4`}>
                  <feature.icon className="h-full w-full text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-gray-400">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}