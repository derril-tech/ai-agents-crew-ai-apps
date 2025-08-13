import React from 'react';
import { Bot, Zap } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-black/20 backdrop-blur-sm border-b border-white/10">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg blur opacity-30"></div>
              <Bot className="relative w-8 h-8 text-white" />
            </div>
            <h1 className="text-xl font-bold text-white">Sales Pitch Assistant</h1>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-gray-300">
              <Zap className="w-4 h-4" />
              <span className="text-sm">AI Powered</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

