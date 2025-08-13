'use client'

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  Users, 
  Mail, 
  BarChart3, 
  Settings, 
  Zap,
  Target,
  Heart
} from 'lucide-react'

const navigation = [
  { name: 'Dashboard', href: '/', icon: Target },
  { name: 'Leads', href: '/leads', icon: Users },
  { name: 'Emails', href: '/emails', icon: Mail },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'AI Tools', href: '/ai-tools', icon: Zap },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <div className="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
      {/* Logo and Branding */}
      <div className="flex flex-col items-center justify-center h-24 border-b border-gray-200 dark:border-gray-700 p-4">
        <div className="flex items-center space-x-2 mb-2">
          <Target className="w-8 h-8 text-blue-600" />
          <span className="text-xl font-bold text-gray-900 dark:text-white">SDR Assistant</span>
        </div>
        <div className="text-center">
          <div className="text-sm font-semibold text-blue-600 dark:text-blue-400">
            AI-Powered Sales Development
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6">
        <ul className="space-y-2">
          {navigation.map((item) => {
            const isActive = pathname === item.href
            return (
              <li key={item.name}>
                <Link
                  href={item.href}
                  className={`flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                  }`}
                >
                  <item.icon className="w-5 h-5" />
                  <span>{item.name}</span>
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>

      {/* Footer with Credits */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700">
        <div className="text-center space-y-2">
          <div className="text-xs text-gray-500 dark:text-gray-400">
            SDR Assistant v1.0.0
          </div>
          <div className="flex items-center justify-center space-x-1 text-xs text-gray-400 dark:text-gray-500">
            <span>Built with</span>
            <Heart className="w-3 h-3 text-red-500" />
            <span>for modern sales teams</span>
          </div>
        </div>
      </div>
    </div>
  )
}
