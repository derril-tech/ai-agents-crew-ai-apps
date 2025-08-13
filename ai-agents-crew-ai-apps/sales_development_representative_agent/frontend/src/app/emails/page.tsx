"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Mail, 
  Plus, 
  Search, 
  Filter,
  Download,
  Send,
  Edit,
  Trash2,
  Eye,
  Copy,
  RefreshCw,
  Calendar,
  Users,
  Target
} from 'lucide-react';

// Mock email data
const mockEmails = [
  {
    id: '1',
    subject: 'AI-Powered Sales Development for Your Team',
    recipient: 'john.smith@techcorp.com',
    leadName: 'John Smith',
    company: 'TechCorp Inc',
    status: 'sent',
    sentDate: '2025-08-12',
    openRate: 85,
    clickRate: 23,
    replyRate: 12,
    template: 'cold-outreach-v1',
    content: 'Hi John, I noticed TechCorp is expanding their engineering team...'
  },
  {
    id: '2',
    subject: 'Streamline Your Sales Process with AI',
    recipient: 'sarah.johnson@innovate.com',
    leadName: 'Sarah Johnson',
    company: 'Innovate Solutions',
    status: 'draft',
    sentDate: null,
    openRate: null,
    clickRate: null,
    replyRate: null,
    template: 'follow-up-v2',
    content: 'Hi Sarah, Following up on our previous conversation...'
  },
  {
    id: '3',
    subject: 'Transform Your Lead Generation Strategy',
    recipient: 'mike.chen@growthco.com',
    leadName: 'Mike Chen',
    company: 'GrowthCo',
    status: 'scheduled',
    sentDate: '2025-08-15',
    openRate: null,
    clickRate: null,
    replyRate: null,
    template: 'value-proposition-v1',
    content: 'Hi Mike, I wanted to share how we helped similar companies...'
  }
];

const EmailCard = ({ email, onView, onEdit, onDelete, onSend, onCopy }) => {
  const getStatusColor = (status) => {
    const colors = {
      draft: 'bg-gray-100 text-gray-800',
      scheduled: 'bg-blue-100 text-blue-800',
      sent: 'bg-green-100 text-green-800',
      opened: 'bg-purple-100 text-purple-800',
      replied: 'bg-indigo-100 text-indigo-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-all duration-200"
    >
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-1">
              {email.subject}
            </h3>
            <p className="text-gray-600 text-sm">
              To: {email.leadName} at {email.company}
            </p>
          </div>
          <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(email.status)}`}>
            {email.status.toUpperCase()}
          </span>
        </div>

        {/* Email Preview */}
        <div className="mb-4">
          <p className="text-gray-700 text-sm line-clamp-2">
            {email.content}
          </p>
        </div>

        {/* Stats */}
        {email.status === 'sent' && (
          <div className="grid grid-cols-3 gap-4 mb-4 p-3 bg-gray-50 rounded-lg">
            <div className="text-center">
              <p className="text-sm text-gray-600">Open Rate</p>
              <p className="text-lg font-semibold text-gray-900">{email.openRate}%</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-600">Click Rate</p>
              <p className="text-lg font-semibold text-gray-900">{email.clickRate}%</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-600">Reply Rate</p>
              <p className="text-lg font-semibold text-gray-900">{email.replyRate}%</p>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <Calendar className="w-4 h-4" />
            <span>{email.sentDate || 'Not sent yet'}</span>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => onView(email)}
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              title="View Email"
            >
              <Eye className="w-4 h-4" />
            </button>
            <button
              onClick={() => onCopy(email)}
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              title="Copy Email"
            >
              <Copy className="w-4 h-4" />
            </button>
            {email.status === 'draft' && (
              <button
                onClick={() => onEdit(email)}
                className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                title="Edit Email"
              >
                <Edit className="w-4 h-4" />
              </button>
            )}
            {email.status === 'draft' && (
              <button
                onClick={() => onSend(email)}
                className="p-2 text-green-400 hover:text-green-600 transition-colors"
                title="Send Email"
              >
                <Send className="w-4 h-4" />
              </button>
            )}
            <button
              onClick={() => onDelete(email.id)}
              className="p-2 text-red-400 hover:text-red-600 transition-colors"
              title="Delete Email"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

const EmailsPage = () => {
  const [emails, setEmails] = useState(mockEmails);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedEmail, setSelectedEmail] = useState(null);
  const [showEmailDetail, setShowEmailDetail] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Filter emails based on search and status
  const filteredEmails = emails.filter(email => {
    const matchesSearch = email.subject.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         email.leadName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         email.company.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = filterStatus === 'all' || email.status === filterStatus;
    
    return matchesSearch && matchesStatus;
  });

  const handleViewEmail = (email) => {
    setSelectedEmail(email);
    setShowEmailDetail(true);
  };

  const handleEditEmail = (email) => {
    // Implement edit functionality
    console.log('Edit email:', email);
  };

  const handleDeleteEmail = (emailId) => {
    if (confirm('Are you sure you want to delete this email?')) {
      setEmails(emails.filter(email => email.id !== emailId));
    }
  };

  const handleSendEmail = (email) => {
    if (confirm('Are you sure you want to send this email?')) {
      setEmails(emails.map(e => 
        e.id === email.id ? { ...e, status: 'sent', sentDate: new Date().toISOString().split('T')[0] } : e
      ));
    }
  };

  const handleCopyEmail = (email) => {
    navigator.clipboard.writeText(email.content);
    alert('Email content copied to clipboard!');
  };

  const stats = {
    total: emails.length,
    sent: emails.filter(e => e.status === 'sent').length,
    drafts: emails.filter(e => e.status === 'draft').length,
    scheduled: emails.filter(e => e.status === 'scheduled').length
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
            Email Management
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Manage your email campaigns, templates, and track performance
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <button
            onClick={() => setShowCreateForm(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center"
          >
            <Plus className="w-4 h-4 mr-2" />
            Create Email
          </button>
          <button
            onClick={() => setIsLoading(true)}
            disabled={isLoading}
            className="bg-green-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-green-700 transition-colors flex items-center disabled:opacity-50"
          >
            {isLoading ? (
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <Send className="w-4 h-4 mr-2" />
            )}
            Send All Drafts
          </button>
        </div>
      </motion.div>

      {/* Stats Cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-2 lg:grid-cols-4 gap-4"
      >
        {[
          { label: 'Total Emails', value: stats.total, icon: Mail, color: 'blue' },
          { label: 'Sent', value: stats.sent, icon: Send, color: 'green' },
          { label: 'Drafts', value: stats.drafts, icon: Edit, color: 'orange' },
          { label: 'Scheduled', value: stats.scheduled, icon: Calendar, color: 'purple' }
        ].map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 + index * 0.05 }}
            className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
              <div className={`p-3 rounded-lg ${
                stat.color === 'blue' ? 'bg-blue-100' :
                stat.color === 'green' ? 'bg-green-100' :
                stat.color === 'orange' ? 'bg-orange-100' : 'bg-purple-100'
              }`}>
                <stat.icon className={`w-6 h-6 ${
                  stat.color === 'blue' ? 'text-blue-600' :
                  stat.color === 'green' ? 'text-green-600' :
                  stat.color === 'orange' ? 'text-orange-600' : 'text-purple-600'
                }`} />
              </div>
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Controls */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
      >
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          {/* Search and Filter */}
          <div className="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-3 flex-1">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search emails..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="pl-10 pr-8 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none bg-white"
              >
                <option value="all">All Status</option>
                <option value="draft">Draft</option>
                <option value="scheduled">Scheduled</option>
                <option value="sent">Sent</option>
                <option value="opened">Opened</option>
                <option value="replied">Replied</option>
              </select>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-3">
            <button 
              onClick={() => {
                const csvContent = [
                  'Subject,Recipient,Status,Sent Date,Open Rate,Click Rate,Reply Rate',
                  ...emails.map(email => [
                    `"${email.subject}"`,
                    `"${email.recipient}"`,
                    email.status,
                    email.sentDate || '',
                    email.openRate || '',
                    email.clickRate || '',
                    email.replyRate || ''
                  ].join(','))
                ].join('\n');

                const blob = new Blob([csvContent], { type: 'text/csv' });
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = `emails_export_${new Date().toISOString().split('T')[0]}.csv`;
                link.click();
              }}
              className="border border-gray-300 text-gray-700 px-4 py-2 rounded-lg font-medium hover:bg-gray-50 transition-colors flex items-center"
            >
              <Download className="w-4 h-4 mr-2" />
              Export
            </button>
          </div>
        </div>
      </motion.div>

      {/* Emails Grid */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        {filteredEmails.length === 0 ? (
          <div className="bg-white rounded-xl p-12 shadow-sm border border-gray-200 text-center">
            <Mail className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No emails found</h3>
            <p className="text-gray-600 mb-6">
              {searchTerm || filterStatus !== 'all' 
                ? 'Try adjusting your search or filter criteria'
                : 'Get started by creating your first email'
              }
            </p>
            {!searchTerm && filterStatus === 'all' && (
              <button
                onClick={() => setShowCreateForm(true)}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center mx-auto"
              >
                <Plus className="w-4 h-4 mr-2" />
                Create Email
              </button>
            )}
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <AnimatePresence>
              {filteredEmails.map((email) => (
                <EmailCard
                  key={email.id}
                  email={email}
                  onView={handleViewEmail}
                  onEdit={handleEditEmail}
                  onDelete={handleDeleteEmail}
                  onSend={handleSendEmail}
                  onCopy={handleCopyEmail}
                />
              ))}
            </AnimatePresence>
          </div>
        )}
      </motion.div>

      {/* Email Detail Modal */}
      <AnimatePresence>
        {showEmailDetail && selectedEmail && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
            onClick={() => setShowEmailDetail(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-white rounded-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-semibold text-gray-900">Email Details</h3>
                <button
                  onClick={() => setShowEmailDetail(false)}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Subject</label>
                  <p className="text-gray-900 font-medium">{selectedEmail.subject}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">To</label>
                  <p className="text-gray-900">{selectedEmail.leadName} ({selectedEmail.recipient})</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Company</label>
                  <p className="text-gray-900">{selectedEmail.company}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Status</label>
                  <span className={`inline-flex px-3 py-1 rounded-full text-sm font-medium ${
                    selectedEmail.status === 'sent' ? 'bg-green-100 text-green-800' :
                    selectedEmail.status === 'draft' ? 'bg-gray-100 text-gray-800' :
                    'bg-blue-100 text-blue-800'
                  }`}>
                    {selectedEmail.status.toUpperCase()}
                  </span>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Content</label>
                  <div className="mt-2 p-4 bg-gray-50 rounded-lg">
                    <p className="text-gray-900 whitespace-pre-wrap">{selectedEmail.content}</p>
                  </div>
                </div>
                {selectedEmail.status === 'sent' && (
                  <div className="grid grid-cols-3 gap-4 p-4 bg-blue-50 rounded-lg">
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Open Rate</p>
                      <p className="text-lg font-semibold text-gray-900">{selectedEmail.openRate}%</p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Click Rate</p>
                      <p className="text-lg font-semibold text-gray-900">{selectedEmail.clickRate}%</p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Reply Rate</p>
                      <p className="text-lg font-semibold text-gray-900">{selectedEmail.replyRate}%</p>
                    </div>
                  </div>
                )}
              </div>

              <div className="flex justify-end space-x-3 mt-6 pt-6 border-t border-gray-200">
                <button
                  onClick={() => setShowEmailDetail(false)}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
                >
                  Close
                </button>
                <button
                  onClick={() => handleCopyEmail(selectedEmail)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
                >
                  Copy Content
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default EmailsPage;
