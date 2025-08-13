"use client";

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Users, ArrowRight } from 'lucide-react';

const LeadsPage = () => {
  const router = useRouter();

  useEffect(() => {
    // Redirect to main dashboard which has comprehensive lead management
    router.push('/');
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="text-center">
        <Users className="w-16 h-16 text-blue-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Redirecting to Lead Management</h2>
        <p className="text-gray-600 mb-4">
          The comprehensive lead management system is available on the main dashboard.
        </p>
        <div className="flex items-center justify-center space-x-2 text-blue-600">
          <span>Redirecting...</span>
          <ArrowRight className="w-4 h-4 animate-pulse" />
        </div>
      </div>
    </div>
  );
};

export default LeadsPage;
