import React from 'react';

export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4">
        <h1 className="text-2xl font-bold text-gray-900">
          AI Code Review Assistant
        </h1>
        <p className="text-gray-600 mt-1">
          Automated code analysis and refactoring suggestions
        </p>
      </div>
    </header>
  );
}