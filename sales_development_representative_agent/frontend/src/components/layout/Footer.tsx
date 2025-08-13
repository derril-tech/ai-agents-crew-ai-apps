'use client'

import React from 'react'
import { Heart, Github, Mail } from 'lucide-react'

export function Footer() {
  return (
    <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-6">
      <div className="container mx-auto px-4 max-w-7xl">
        <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
          {/* Left side - App Info */}
          <div className="flex items-center space-x-4">
            <div className="text-sm text-gray-600 dark:text-gray-400">
              SDR Assistant - AI-Powered Sales Development
            </div>
          </div>

          {/* Center - App Info */}
          <div className="text-center">
            <div className="flex items-center justify-center space-x-1 text-xs text-gray-400 dark:text-gray-500">
              <span>Built with</span>
              <Heart className="w-3 h-3 text-red-500" />
              <span>for modern sales teams</span>
            </div>
          </div>

          {/* Right side - Social Links */}
          <div className="flex items-center space-x-4">
            <div className="text-xs text-gray-500 dark:text-gray-400">
              © 2025 SDR Assistant
            </div>
            <div className="flex items-center space-x-2">
              <a 
                href="https://github.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
              >
                <Github className="w-4 h-4" />
              </a>
              <a 
                href="mailto:contact@sdr-assistant.com" 
                className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
              >
                <Mail className="w-4 h-4" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
