'use client'

import React from 'react'
import { Bell, User } from 'lucide-react'

export function Header() {

  return (
    <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Left side - App Title */}
        <div className="flex items-center space-x-6">
          <div className="text-left">
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">SDR Assistant</h1>
            <p className="text-sm text-gray-500 dark:text-gray-400">Lead Management Dashboard</p>
          </div>
        </div>

        {/* Right side - User menu and notifications */}
        <div className="flex items-center space-x-4">
          {/* Notifications */}
          <button className="relative p-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors">
            <Bell className="w-5 h-5" />
            <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400"></span>
          </button>

          {/* User menu */}
          <div className="flex items-center space-x-3">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900 dark:text-white">SDR Assistant</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">AI-Powered Sales Development</p>
            </div>
            <button className="flex items-center justify-center w-8 h-8 bg-gray-200 dark:bg-gray-700 rounded-full">
              <User className="w-4 h-4 text-gray-600 dark:text-gray-300" />
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
