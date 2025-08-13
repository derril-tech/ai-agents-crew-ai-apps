// dashboard/page.tsx
// frontend/app/dashboard/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useAuthStore } from '@/stores/authStore';
import { useEmailStore } from '@/stores/emailStore';
import { useAgentStore } from '@/stores/agentStore';
import DashboardLayout from '@/components/layouts/DashboardLayout';
import EmailQueue from '@/components/features/EmailQueue';
import AgentActivity from '@/components/features/AgentActivity';
import DraftEditor from '@/components/features/DraftEditor';
import Analytics from '@/components/features/Analytics';
import { motion } from 'framer-motion';
import { 
  Mail, Bot, TrendingUp, Clock, 
  CheckCircle, AlertCircle, Loader2 
} from 'lucide-react';

export default function DashboardPage() {
  const { user, checkAuth } = useAuthStore();
  const { emails, fetchUnreadEmails, stats } = useEmailStore();
  const { agentStatus, startAgent, stopAgent, isRunning } = useAgentStore();
  const [selectedTab, setSelectedTab] = useState<'emails' | 'agents' | 'drafts' | 'analytics'>('emails');
  const [selectedEmail, setSelectedEmail] = useState<any>(null);

  useEffect(() => {
    checkAuth();
    fetchUnreadEmails();
  }, []);

  const statsCards = [
    {
      title: 'Unread Emails',
      value: emails.filter(e => e.is_unread).length,
      icon: Mail,
      color: 'from-blue-500 to-cyan-500',
      change: '+12%',
    },
    {
      title: 'Processing',
      value: agentStatus?.statistics?.emails_processed || 0,
      icon: Bot,
      color: 'from-purple-500 to-pink-500',
      change: '+5%',
    },
    {
      title: 'Drafts Created',
      value: agentStatus?.statistics?.drafts_created || 0,
      icon: CheckCircle,
      color: 'from-green-500 to-emerald-500',
      change: '+8%',
    },
    {
      title: 'Avg Response Time',
      value: '2.5m',
      icon: Clock,
      color: 'from-orange-500 to-red-500',
      change: '-15%',
    },
  ];

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        {/* Header */}
        <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
          <div className="px-6 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                  Email Dashboard
                </h1>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Welcome back, {user?.email || 'User'}
                </p>
              </div>
              
              {/* Agent Control */}
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className={`w-2 h-2 rounded-full ${isRunning ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`} />
                  <span className="text-sm text-gray-600 dark:text-gray-300">
                    Agent {isRunning ? 'Active' : 'Inactive'}
                  </span>
                </div>
                
                <button
                  onClick={() => isRunning ? stopAgent() : startAgent()}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    isRunning
                      ? 'bg-red-500 hover:bg-red-600 text-white'
                      : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white'
                  }`}
                >
                  {isRunning ? 'Stop Agent' : 'Start Agent'}
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="px-6 py-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {statsCards.map((stat, index) => (
              <motion.div
                key={stat.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${stat.color} p-2.5`}>
                    <stat.icon className="h-full w-full text-white" />
                  </div>
                  <span className={`text-sm font-medium ${
                    stat.change.startsWith('+') ? 'text-green-500' : 'text-red-500'
                  }`}>
                    {stat.change}
                  </span>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stat.value}
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {stat.title}
                </p>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Tabs */}
        <div className="px-6">
          <div className="border-b border-gray-200 dark:border-gray-700">
            <nav className="flex space-x-8">
              {['emails', 'agents', 'drafts', 'analytics'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setSelectedTab(tab as any)}
                  className={`py-2 px-1 border-b-2 font-medium text-sm capitalize transition-colors ${
                    selectedTab === tab
                      ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                      : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
                  }`}
                >
                  {tab}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Content */}
        <div className="px-6 py-6">
          <motion.div
            key={selectedTab}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
          >
            {selectedTab === 'emails' && (
              <div className="grid lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2">
                  <EmailQueue 
                    emails={emails}
                    onSelectEmail={setSelectedEmail}
                    selectedEmail={selectedEmail}
                  />
                </div>
                <div>
                  {selectedEmail && (
                    <DraftEditor
                      email={selectedEmail}
                      onClose={() => setSelectedEmail(null)}
                    />
                  )}
                </div>
              </div>
            )}

            {selectedTab === 'agents' && (
              <AgentActivity status={agentStatus} />
            )}

            {selectedTab === 'drafts' && (
              <div className="bg-white dark:bg-gray-800 rounded-xl p-6">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                  Draft Management
                </h2>
                <DraftEditor email={null} onClose={() => {}} />
              </div>
            )}

            {selectedTab === 'analytics' && (
              <Analytics />
            )}
          </motion.div>
        </div>
      </div>
    </DashboardLayout>
  );
}