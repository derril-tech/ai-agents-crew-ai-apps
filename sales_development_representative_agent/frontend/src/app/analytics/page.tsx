"use client";

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  Mail, 
  Target, 
  Calendar,
  Download,
  Filter,
  RefreshCw
} from 'lucide-react';

// Mock analytics data
const mockAnalytics = {
  overview: {
    totalLeads: 1247,
    conversionRate: 23.4,
    avgResponseTime: 2.3,
    revenueGenerated: 456000
  },
  monthlyTrends: [
    { month: 'Jan', leads: 89, conversions: 12, revenue: 45000 },
    { month: 'Feb', leads: 102, conversions: 18, revenue: 52000 },
    { month: 'Mar', leads: 156, conversions: 24, revenue: 68000 },
    { month: 'Apr', leads: 134, conversions: 19, revenue: 58000 },
    { month: 'May', leads: 178, conversions: 31, revenue: 72000 },
    { month: 'Jun', leads: 203, conversions: 38, revenue: 85000 },
    { month: 'Jul', leads: 189, conversions: 35, revenue: 78000 },
    { month: 'Aug', leads: 156, conversions: 28, revenue: 64000 }
  ],
  leadSources: [
    { source: 'LinkedIn', count: 456, conversionRate: 28.5 },
    { source: 'Website', count: 234, conversionRate: 18.2 },
    { source: 'Referrals', count: 189, conversionRate: 32.1 },
    { source: 'Conferences', count: 156, conversionRate: 25.6 },
    { source: 'Cold Email', count: 212, conversionRate: 15.8 }
  ],
  topPerformers: [
    { name: 'Sarah Johnson', leads: 89, conversions: 23, revenue: 125000 },
    { name: 'Mike Chen', leads: 76, conversions: 19, revenue: 98000 },
    { name: 'Emily Davis', leads: 67, conversions: 16, revenue: 87000 },
    { name: 'Alex Rodriguez', leads: 54, conversions: 14, revenue: 72000 }
  ]
};

const AnalyticsPage = () => {
  const [timeRange, setTimeRange] = useState('30d');
  const [isLoading, setIsLoading] = useState(false);
  const [analytics, setAnalytics] = useState(mockAnalytics);

  const handleRefresh = async () => {
    setIsLoading(true);
    // Simulate API call
    setTimeout(() => {
      setAnalytics(mockAnalytics);
      setIsLoading(false);
    }, 1000);
  };

  const handleExport = () => {
    // Create CSV export
    const csvContent = [
      'Metric,Value',
      `Total Leads,${analytics.overview.totalLeads}`,
      `Conversion Rate,${analytics.overview.conversionRate}%`,
      `Avg Response Time,${analytics.overview.avgResponseTime} days`,
      `Revenue Generated,$${analytics.overview.revenueGenerated.toLocaleString()}`
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `analytics_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col sm:flex-row sm:items-center sm:justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Analytics Dashboard
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Track your sales performance and optimize your outreach strategy
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
            <option value="1y">Last year</option>
          </select>
          <button
            onClick={handleRefresh}
            disabled={isLoading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center disabled:opacity-50"
          >
            {isLoading ? (
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <RefreshCw className="w-4 h-4 mr-2" />
            )}
            Refresh
          </button>
          <button
            onClick={handleExport}
            className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors flex items-center"
          >
            <Download className="w-4 h-4 mr-2" />
            Export
          </button>
        </div>
      </motion.div>

      {/* Overview Cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {[
          {
            label: 'Total Leads',
            value: analytics.overview.totalLeads.toLocaleString(),
            icon: Users,
            color: 'blue',
            change: '+12.5%'
          },
          {
            label: 'Conversion Rate',
            value: `${analytics.overview.conversionRate}%`,
            icon: Target,
            color: 'green',
            change: '+2.1%'
          },
          {
            label: 'Avg Response Time',
            value: `${analytics.overview.avgResponseTime} days`,
            icon: Calendar,
            color: 'orange',
            change: '-0.5 days'
          },
          {
            label: 'Revenue Generated',
            value: `$${analytics.overview.revenueGenerated.toLocaleString()}`,
            icon: TrendingUp,
            color: 'purple',
            change: '+18.3%'
          }
        ].map((metric, index) => (
          <motion.div
            key={metric.label}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 + index * 0.05 }}
            className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">{metric.label}</p>
                <p className="text-2xl font-bold text-gray-900">{metric.value}</p>
                <p className="text-sm text-green-600 mt-1">{metric.change} vs last period</p>
              </div>
              <div className={`p-3 rounded-lg ${
                metric.color === 'blue' ? 'bg-blue-100' :
                metric.color === 'green' ? 'bg-green-100' :
                metric.color === 'orange' ? 'bg-orange-100' : 'bg-purple-100'
              }`}>
                <metric.icon className={`w-6 h-6 ${
                  metric.color === 'blue' ? 'text-blue-600' :
                  metric.color === 'green' ? 'text-green-600' :
                  metric.color === 'orange' ? 'text-orange-600' : 'text-purple-600'
                }`} />
              </div>
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Trends */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Monthly Trends</h3>
          <div className="space-y-4">
            {analytics.monthlyTrends.map((month, index) => (
              <div key={month.month} className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">{month.month}</span>
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <p className="text-sm text-gray-600">Leads: {month.leads}</p>
                    <p className="text-sm text-gray-600">Revenue: ${month.revenue.toLocaleString()}</p>
                  </div>
                  <div className="w-24 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${(month.conversions / 40) * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Lead Sources */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Lead Sources</h3>
          <div className="space-y-4">
            {analytics.leadSources.map((source, index) => (
              <div key={source.source} className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className={`w-3 h-3 rounded-full ${
                    index === 0 ? 'bg-blue-500' :
                    index === 1 ? 'bg-green-500' :
                    index === 2 ? 'bg-purple-500' :
                    index === 3 ? 'bg-orange-500' : 'bg-red-500'
                  }`} />
                  <span className="text-sm font-medium text-gray-700">{source.source}</span>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">{source.count} leads</p>
                  <p className="text-sm text-gray-600">{source.conversionRate}% conversion</p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Top Performers */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Performers</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-medium text-gray-700">Name</th>
                <th className="text-right py-3 px-4 font-medium text-gray-700">Leads</th>
                <th className="text-right py-3 px-4 font-medium text-gray-700">Conversions</th>
                <th className="text-right py-3 px-4 font-medium text-gray-700">Revenue</th>
                <th className="text-right py-3 px-4 font-medium text-gray-700">Conversion Rate</th>
              </tr>
            </thead>
            <tbody>
              {analytics.topPerformers.map((performer, index) => (
                <tr key={performer.name} className="border-b border-gray-100">
                  <td className="py-3 px-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                        <span className="text-sm font-medium text-blue-600">
                          {performer.name.split(' ').map(n => n[0]).join('')}
                        </span>
                      </div>
                      <span className="font-medium text-gray-900">{performer.name}</span>
                    </div>
                  </td>
                  <td className="text-right py-3 px-4 text-gray-900">{performer.leads}</td>
                  <td className="text-right py-3 px-4 text-gray-900">{performer.conversions}</td>
                  <td className="text-right py-3 px-4 text-gray-900">${performer.revenue.toLocaleString()}</td>
                  <td className="text-right py-3 px-4 text-gray-900">
                    {((performer.conversions / performer.leads) * 100).toFixed(1)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  );
};

export default AnalyticsPage;
