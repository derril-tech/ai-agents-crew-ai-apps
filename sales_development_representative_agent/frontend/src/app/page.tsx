"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Users, 
  Plus, 
  Upload, 
  Search, 
  Filter,
  Download,
  BarChart3,
  Mail,
  Target,
  Zap,
  Eye,
  Edit,
  Trash2,
  RefreshCw
} from 'lucide-react';
import Image from 'next/image';

// Mock data for demonstration
const mockLeads = [
  {
    id: '1',
    name: 'Mark Benioff',
    jobTitle: 'CEO',
    company: 'Salesforce',
    email: 'mark@salesforce.com',
    score: 92,
    status: 'analyzed',
    industry: 'Technology',
    companySize: 'Enterprise',
    lastContact: '2025-08-10',
    source: 'Conference'
  },
  {
    id: '2',
    name: 'Satya Nadella',
    jobTitle: 'CEO',
    company: 'Microsoft',
    email: 'satya@microsoft.com',
    score: 88,
    status: 'email_drafted',
    industry: 'Technology',
    companySize: 'Enterprise',
    lastContact: '2025-08-09',
    source: 'LinkedIn'
  },
  {
    id: '3',
    name: 'Jensen Huang',
    jobTitle: 'CEO',
    company: 'NVIDIA',
    email: 'jensen@nvidia.com',
    score: 95,
    status: 'new',
    industry: 'Technology',
    companySize: 'Large',
    lastContact: null,
    source: 'Partner Referral'
  }
];

const LeadCard = ({ lead, onView, onEdit, onDelete }) => {
  // Defensive programming: ensure all required properties exist
  const safeLead = {
    id: lead.id || '',
    name: lead.name || 'Unknown',
    jobTitle: lead.jobTitle || 'Unknown',
    company: lead.company || 'Unknown',
    email: lead.email || '',
    score: lead.score || 0,
    status: lead.status || 'new',
    industry: lead.industry || 'Technology',
    companySize: lead.companySize || 'Medium',
    lastContact: lead.lastContact || null,
    source: lead.source || 'Unknown',
    linkedinUrl: lead.linkedinUrl || '',
    companyWebsite: lead.companyWebsite || '',
    useCase: lead.useCase || ''
  };

  const getStatusColor = (status) => {
    const colors = {
      new: 'bg-blue-100 text-blue-800',
      analyzing: 'bg-yellow-100 text-yellow-800',
      analyzed: 'bg-green-100 text-green-800',
      email_drafted: 'bg-purple-100 text-purple-800',
      email_sent: 'bg-indigo-100 text-indigo-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-50';
    if (score >= 60) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
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
              {safeLead.name}
            </h3>
            <p className="text-gray-600 text-sm">
              {safeLead.jobTitle} at {safeLead.company}
            </p>
          </div>
          <div className={`px-3 py-1 rounded-full text-xs font-medium ${getScoreColor(safeLead.score)}`}>
            Score: {safeLead.score}
          </div>
        </div>

        {/* Details */}
        <div className="space-y-2 mb-4">
          <div className="flex items-center text-sm text-gray-600">
            <Target className="w-4 h-4 mr-2" />
            <span>{safeLead.industry} • {safeLead.companySize}</span>
          </div>
          <div className="flex items-center text-sm text-gray-600">
            <Mail className="w-4 h-4 mr-2" />
            <span className="truncate">{safeLead.email}</span>
          </div>
        </div>

        {/* Status */}
        <div className="flex items-center justify-between mb-4">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(safeLead.status)}`}>
            {safeLead.status.replace('_', ' ').toUpperCase()}
          </span>
          <span className="text-xs text-gray-500">
            Source: {safeLead.source}
          </span>
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-2">
          <button
            onClick={() => onView(safeLead)}
            className="flex-1 bg-blue-600 text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors flex items-center justify-center"
          >
            <Eye className="w-4 h-4 mr-1" />
            View
          </button>
          <button
            onClick={() => onEdit(safeLead)}
            className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg text-sm hover:bg-gray-50 transition-colors"
          >
            <Edit className="w-4 h-4" />
          </button>
          <button
            onClick={() => onDelete(safeLead.id)}
            className="px-3 py-2 border border-red-300 text-red-600 rounded-lg text-sm hover:bg-red-50 transition-colors"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </motion.div>
  );
};

const LeadsPage = () => {
  const [leads, setLeads] = useState(mockLeads);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [isLoading, setIsLoading] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newLead, setNewLead] = useState({
    name: '',
    jobTitle: '',
    company: '',
    email: '',
    linkedinUrl: '',
    companyWebsite: '',
    useCase: '',
    source: ''
  });
  const [selectedLead, setSelectedLead] = useState(null);
  const [showLeadDetail, setShowLeadDetail] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [editingLead, setEditingLead] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [serverStatus, setServerStatus] = useState('checking');
  const [generatingEmail, setGeneratingEmail] = useState(false);

  // Load leads from backend on component mount
  useEffect(() => {
    const loadLeads = async () => {
      try {
        // First check server health
        const healthResponse = await fetch('http://localhost:8000/health');
        if (healthResponse.ok) {
          setServerStatus('connected');
        } else {
          setServerStatus('error');
        }

        const response = await fetch('http://localhost:8000/api/leads');
        if (response.ok) {
          const data = await response.json();
          setLeads(data.leads || data || []);
        } else {
          console.error('Failed to load leads from backend, using mock data');
          setLeads(mockLeads);
        }
      } catch (error) {
        console.error('Error loading leads:', error);
        console.log('Using mock data as fallback');
        setLeads(mockLeads);
        setServerStatus('error');
      }
    };

    loadLeads();
  }, []);

  // Filter leads based on search and status
  const filteredLeads = leads.filter(lead => {
    // Defensive programming: ensure all required properties exist
    const name = lead.name || '';
    const company = lead.company || '';
    const jobTitle = lead.jobTitle || '';
    const status = lead.status || 'new';
    
    const matchesSearch = name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         jobTitle.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = filterStatus === 'all' || status === filterStatus;
    
    return matchesSearch && matchesStatus;
  });

  const handleViewLead = (lead) => {
    setSelectedLead(lead);
    setShowLeadDetail(true);
  };

  const handleEditLead = (lead) => {
    setEditingLead({ ...lead });
    setShowEditForm(true);
  };

  const handleUpdateLead = async (e) => {
    e.preventDefault();
    if (!editingLead.name || !editingLead.jobTitle || !editingLead.company || !editingLead.email) {
      alert('Please fill in all required fields (Name, Job Title, Company, Email)');
      return;
    }

    setIsSubmitting(true);
    try {
      // Call backend API to update lead
      const response = await fetch(`http://localhost:8000/api/leads/${editingLead.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editingLead),
      });

      if (response.ok) {
        // Update local state
        setLeads(leads.map(lead => 
          lead.id === editingLead.id ? editingLead : lead
        ));
        setShowEditForm(false);
        setEditingLead(null);
        alert('Lead updated successfully!');
      } else {
        throw new Error('Failed to update lead');
      }
    } catch (error) {
      console.error('Error updating lead:', error);
      alert('Failed to update lead. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteLead = async (leadId) => {
    if (!confirm('Are you sure you want to delete this lead?')) {
      return;
    }

    try {
      // Call backend API to delete lead
      const response = await fetch(`http://localhost:8000/api/leads/${leadId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setLeads(leads.filter(lead => lead.id !== leadId));
        alert('Lead deleted successfully!');
      } else {
        throw new Error('Failed to delete lead');
      }
    } catch (error) {
      console.error('Error deleting lead:', error);
      alert('Failed to delete lead. Please try again.');
    }
  };

  const handleBulkAnalysis = async () => {
    setIsLoading(true);
    try {
      // Call backend API for bulk analysis
      const response = await fetch('http://localhost:8000/api/leads/analyze-bulk', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ leadIds: leads.map(lead => lead.id) }),
      });

      if (response.ok) {
        const result = await response.json();
        // Update leads with analysis results
        setLeads(leads.map(lead => {
          const analyzedLead = result.leads.find(l => l.id === lead.id);
          return analyzedLead ? { ...lead, ...analyzedLead } : lead;
        }));
        alert(`Successfully analyzed ${result.leads.length} leads!`);
      } else {
        throw new Error('Failed to analyze leads');
      }
    } catch (error) {
      console.error('Error analyzing leads:', error);
      alert('Failed to analyze leads. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateEmail = async (lead) => {
    setGeneratingEmail(true);
    try {
      // Call backend API to generate email
      const response = await fetch('http://localhost:8000/api/emails/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ leadId: lead.id }),
      });

      if (response.ok) {
        const result = await response.json();
        alert(`Email generated successfully!\n\nSubject: ${result.subject}\n\n${result.content}`);
        
        // Update lead status to email_drafted
        setLeads(leads.map(l => 
          l.id === lead.id ? { ...l, status: 'email_drafted' } : l
        ));
      } else {
        throw new Error('Failed to generate email');
      }
    } catch (error) {
      console.error('Error generating email:', error);
      alert('Failed to generate email. Please try again.');
    } finally {
      setGeneratingEmail(false);
    }
  };

  const handleAddLead = async (e) => {
    e.preventDefault();
    if (!newLead.name || !newLead.jobTitle || !newLead.company || !newLead.email) {
      alert('Please fill in all required fields (Name, Job Title, Company, Email)');
      return;
    }

    setIsSubmitting(true);
    try {
      const leadData = {
        name: newLead.name,
        jobTitle: newLead.jobTitle,
        company: newLead.company,
        email: newLead.email,
        linkedinUrl: newLead.linkedinUrl,
        companyWebsite: newLead.companyWebsite,
        useCase: newLead.useCase,
        source: newLead.source || 'Manual Entry',
        score: 0,
        status: 'new',
        industry: 'Technology',
        companySize: 'Medium',
        lastContact: null
      };

      console.log('Sending lead data:', leadData);

      // Call backend API to create lead
      const response = await fetch('http://localhost:8000/api/leads', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(leadData),
      });

      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);

      if (response.ok) {
        const createdLead = await response.json();
        console.log('Created lead:', createdLead);
        setLeads([...leads, createdLead]);
        setNewLead({
          name: '',
          jobTitle: '',
          company: '',
          email: '',
          linkedinUrl: '',
          companyWebsite: '',
          useCase: '',
          source: ''
        });
        setShowAddForm(false);
        alert('Lead added successfully!');
      } else {
        const errorText = await response.text();
        console.error('Server error response:', errorText);
        throw new Error(`Failed to create lead: ${response.status} - ${errorText}`);
      }
    } catch (error) {
      console.error('Error creating lead:', error);
      alert(`Failed to create lead: ${error.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleImportCSV = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.csv';
    input.onchange = (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
          const csv = event.target.result;
          const lines = csv.split('\n');
          const headers = lines[0].split(',').map(h => h.trim());
          
          const importedLeads = lines.slice(1).filter(line => line.trim()).map((line, index) => {
            const values = line.split(',').map(v => v.trim());
            return {
              id: `imported-${Date.now()}-${index}`,
              name: values[0] || '',
              jobTitle: values[1] || '',
              company: values[2] || '',
              email: values[3] || '',
              linkedinUrl: values[4] || '',
              companyWebsite: values[5] || '',
              useCase: values[6] || '',
              source: values[7] || 'CSV Import',
              score: 0,
              status: 'new',
              industry: 'Technology',
              companySize: 'Medium',
              lastContact: null
            };
          });
          
          setLeads([...leads, ...importedLeads]);
          alert(`Successfully imported ${importedLeads.length} leads!`);
        };
        reader.readAsText(file);
      }
    };
    input.click();
  };

  const handleExportLeads = () => {
    if (leads.length === 0) {
      alert('No leads to export!');
      return;
    }

    // Create CSV content
    const headers = ['Name', 'Job Title', 'Company', 'Email', 'LinkedIn URL', 'Company Website', 'Use Case', 'Source', 'Score', 'Status', 'Industry', 'Company Size', 'Last Contact'];
    const csvContent = [
      headers.join(','),
      ...leads.map(lead => [
        `"${lead.name}"`,
        `"${lead.jobTitle}"`,
        `"${lead.company}"`,
        `"${lead.email}"`,
        `"${lead.linkedinUrl || ''}"`,
        `"${lead.companyWebsite || ''}"`,
        `"${lead.useCase || ''}"`,
        `"${lead.source || ''}"`,
        lead.score,
        lead.status,
        `"${lead.industry || ''}"`,
        `"${lead.companySize || ''}"`,
        `"${lead.lastContact || ''}"`
      ].join(','))
    ].join('\n');

    // Create and download file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `leads_export_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const stats = {
    total: leads.length,
    analyzed: leads.filter(l => (l.status || 'new') === 'analyzed').length,
    emailsDrafted: leads.filter(l => (l.status || 'new') === 'email_drafted').length,
    avgScore: leads.length > 0 ? Math.round(leads.reduce((sum, l) => sum + (l.score || 0), 0) / leads.length) : 0
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
           <div className="flex items-center space-x-3 mb-2">
             <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
               Lead Management
             </h1>
             <div className="flex items-center space-x-2">
               <span className="text-sm text-gray-500 dark:text-gray-400">by</span>
               <span className="text-sm font-semibold text-blue-600 dark:text-blue-400">Derril Filemon</span>
               <a 
                 href="https://linkedin.com/in/derril-filemon" 
                 target="_blank" 
                 rel="noopener noreferrer"
                 className="inline-flex items-center justify-center w-6 h-6 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
               >
                 <Image
                   src="/images/linkedin.PNG"
                   alt="LinkedIn"
                   width={20}
                   height={20}
                   className="rounded-sm"
                 />
               </a>
             </div>
           </div>
           <p className="text-gray-600 dark:text-gray-400">
             Analyze, score, and manage your sales prospects with AI-powered insights
           </p>
           <div className="mt-2 flex items-center space-x-3">
             <div className={`flex items-center space-x-2 px-2 py-1 rounded-lg text-xs font-medium ${
               serverStatus === 'connected' ? 'bg-green-100 text-green-800' :
               serverStatus === 'error' ? 'bg-red-100 text-red-800' :
               'bg-yellow-100 text-yellow-800'
             }`}>
               <div className={`w-2 h-2 rounded-full ${
                 serverStatus === 'connected' ? 'bg-green-500' :
                 serverStatus === 'error' ? 'bg-red-500' :
                 'bg-yellow-500 animate-pulse'
               }`}></div>
               <span>
                 {serverStatus === 'connected' ? 'Backend Connected' :
                  serverStatus === 'error' ? 'Backend Offline' :
                  'Checking Backend...'}
               </span>
             </div>
           </div>
         </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <button
            onClick={() => setShowAddForm(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Lead
          </button>
          <button 
            onClick={handleImportCSV}
            className="bg-green-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-green-700 transition-colors flex items-center"
          >
            <Upload className="w-4 h-4 mr-2" />
            Import CSV
          </button>
        </div>
      </motion.div>



       {/* Stats Cards */}
       <motion.div
         initial={{ opacity: 0, y: 20 }}
         animate={{ opacity: 1, y: 0 }}
         transition={{ delay: 0.2 }}
         className="grid grid-cols-2 lg:grid-cols-4 gap-4"
       >
        {[
          { label: 'Total Leads', value: stats.total, icon: Users, color: 'blue' },
          { label: 'Analyzed', value: stats.analyzed, icon: BarChart3, color: 'green' },
          { label: 'Emails Drafted', value: stats.emailsDrafted, icon: Mail, color: 'purple' },
          { label: 'Avg Score', value: stats.avgScore + '/100', icon: Target, color: 'orange' }
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
                stat.color === 'purple' ? 'bg-purple-100' : 'bg-orange-100'
              }`}>
                <stat.icon className={`w-6 h-6 ${
                  stat.color === 'blue' ? 'text-blue-600' :
                  stat.color === 'green' ? 'text-green-600' :
                  stat.color === 'purple' ? 'text-purple-600' : 'text-orange-600'
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
         transition={{ delay: 0.3 }}
         className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
       >
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          {/* Search and Filter */}
          <div className="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-3 flex-1">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search leads..."
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
                <option value="new">New</option>
                <option value="analyzing">Analyzing</option>
                <option value="analyzed">Analyzed</option>
                <option value="email_drafted">Email Drafted</option>
                <option value="email_sent">Email Sent</option>
              </select>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-3">
            <button
              onClick={handleBulkAnalysis}
              disabled={isLoading}
              className="bg-purple-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-purple-700 transition-colors flex items-center disabled:opacity-50"
            >
              {isLoading ? (
                <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
              ) : (
                <Zap className="w-4 h-4 mr-2" />
              )}
              Analyze All
            </button>
            <button 
              onClick={handleExportLeads}
              className="border border-gray-300 text-gray-700 px-4 py-2 rounded-lg font-medium hover:bg-gray-50 transition-colors flex items-center"
            >
              <Download className="w-4 h-4 mr-2" />
              Export
            </button>
          </div>
        </div>
      </motion.div>

             {/* Leads Grid */}
       <motion.div
         initial={{ opacity: 0 }}
         animate={{ opacity: 1 }}
         transition={{ delay: 0.4 }}
       >
        {filteredLeads.length === 0 ? (
          <div className="bg-white rounded-xl p-12 shadow-sm border border-gray-200 text-center">
            <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No leads found</h3>
            <p className="text-gray-600 mb-6">
              {searchTerm || filterStatus !== 'all' 
                ? 'Try adjusting your search or filter criteria'
                : 'Get started by adding your first lead or importing a CSV file'
              }
            </p>
            {!searchTerm && filterStatus === 'all' && (
              <div className="flex justify-center space-x-3">
                <button
                  onClick={() => setShowAddForm(true)}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add Lead
                </button>
                <button 
                  onClick={handleImportCSV}
                  className="border border-gray-300 text-gray-700 px-6 py-2 rounded-lg font-medium hover:bg-gray-50 transition-colors flex items-center"
                >
                  <Upload className="w-4 h-4 mr-2" />
                  Import CSV
                </button>
              </div>
            )}
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <AnimatePresence>
              {filteredLeads.map((lead) => (
                <LeadCard
                  key={lead.id}
                  lead={lead}
                  onView={handleViewLead}
                  onEdit={handleEditLead}
                  onDelete={handleDeleteLead}
                />
              ))}
            </AnimatePresence>
          </div>
        )}
      </motion.div>

      {/* Bulk Processing Status */}
      <AnimatePresence>
        {isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 50 }}
            className="fixed bottom-6 right-6 bg-white rounded-xl p-6 shadow-lg border border-gray-200 max-w-sm"
          >
            <div className="flex items-center space-x-3">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
              <div>
                <h4 className="font-medium text-gray-900">Processing Leads</h4>
                <p className="text-sm text-gray-600">Analyzing {leads.length} leads with AI agents...</p>
              </div>
            </div>
            <div className="mt-3 bg-gray-200 rounded-full h-2">
              <motion.div
                className="bg-purple-600 h-2 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: '100%' }}
                transition={{ duration: 3, ease: "easeInOut" }}
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Add Lead Form Modal */}
      <AnimatePresence>
        {showAddForm && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
            onClick={() => {
              setShowAddForm(false);
              setNewLead({
                name: '',
                jobTitle: '',
                company: '',
                email: '',
                linkedinUrl: '',
                companyWebsite: '',
                useCase: '',
                source: ''
              });
            }}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-white rounded-xl p-6 w-full max-w-md"
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Add New Lead</h3>
              <form onSubmit={handleAddLead} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Name *</label>
                    <input
                      type="text"
                      required
                      value={newLead.name}
                      onChange={(e) => setNewLead({...newLead, name: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="John Smith"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Job Title *</label>
                    <input
                      type="text"
                      required
                      value={newLead.jobTitle}
                      onChange={(e) => setNewLead({...newLead, jobTitle: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="VP of Engineering"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Company *</label>
                    <input
                      type="text"
                      required
                      value={newLead.company}
                      onChange={(e) => setNewLead({...newLead, company: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="TechCorp Inc"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Email *</label>
                    <input
                      type="email"
                      required
                      value={newLead.email}
                      onChange={(e) => setNewLead({...newLead, email: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="john@techcorp.com"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">LinkedIn URL</label>
                    <input
                      type="url"
                      value={newLead.linkedinUrl}
                      onChange={(e) => setNewLead({...newLead, linkedinUrl: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="https://linkedin.com/in/johnsmith"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Company Website</label>
                    <input
                      type="url"
                      value={newLead.companyWebsite}
                      onChange={(e) => setNewLead({...newLead, companyWebsite: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="https://techcorp.com"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Use Case</label>
                  <textarea
                    value={newLead.useCase}
                    onChange={(e) => setNewLead({...newLead, useCase: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows="3"
                    placeholder="Looking to implement AI in development workflow"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Source</label>
                  <select
                    value={newLead.source}
                    onChange={(e) => setNewLead({...newLead, source: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select source</option>
                    <option value="conference">Conference</option>
                    <option value="referral">Referral</option>
                    <option value="website">Website</option>
                    <option value="LinkedIn">LinkedIn</option>
                    <option value="partner">Partner</option>
                    <option value="manual">Manual Entry</option>
                  </select>
                </div>
                <div className="flex space-x-3">
                  <button
                    type="button"
                    onClick={() => {
                      setShowAddForm(false);
                      setNewLead({
                        name: '',
                        jobTitle: '',
                        company: '',
                        email: '',
                        linkedinUrl: '',
                        companyWebsite: '',
                        useCase: '',
                        source: ''
                      });
                    }}
                    className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
                  >
                    Cancel
                  </button>
                                     <button
                     type="submit"
                     disabled={isSubmitting}
                     className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
                   >
                     {isSubmitting ? 'Adding...' : 'Add Lead'}
                   </button>
                </div>
              </form>
            </motion.div>
          </motion.div>
                 )}
       </AnimatePresence>

       {/* Edit Lead Form Modal */}
       <AnimatePresence>
         {showEditForm && editingLead && (
           <motion.div
             initial={{ opacity: 0 }}
             animate={{ opacity: 1 }}
             exit={{ opacity: 0 }}
             className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
             onClick={() => {
               setShowEditForm(false);
               setEditingLead(null);
             }}
           >
             <motion.div
               initial={{ scale: 0.9, opacity: 0 }}
               animate={{ scale: 1, opacity: 1 }}
               exit={{ scale: 0.9, opacity: 0 }}
               className="bg-white rounded-xl p-6 w-full max-w-md"
               onClick={(e) => e.stopPropagation()}
             >
               <h3 className="text-lg font-semibold text-gray-900 mb-4">Edit Lead</h3>
               <form onSubmit={handleUpdateLead} className="space-y-4">
                 <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">Name *</label>
                     <input
                       type="text"
                       required
                       value={editingLead.name}
                       onChange={(e) => setEditingLead({...editingLead, name: e.target.value})}
                       className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                       placeholder="John Smith"
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">Job Title *</label>
                     <input
                       type="text"
                       required
                       value={editingLead.jobTitle}
                       onChange={(e) => setEditingLead({...editingLead, jobTitle: e.target.value})}
                       className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                       placeholder="VP of Engineering"
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">Company *</label>
                     <input
                       type="text"
                       required
                       value={editingLead.company}
                       onChange={(e) => setEditingLead({...editingLead, company: e.target.value})}
                       className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                       placeholder="TechCorp Inc"
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">Email *</label>
                     <input
                       type="email"
                       required
                       value={editingLead.email}
                       onChange={(e) => setEditingLead({...editingLead, email: e.target.value})}
                       className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                       placeholder="john@techcorp.com"
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">LinkedIn URL</label>
                     <input
                       type="url"
                       value={editingLead.linkedinUrl || ''}
                       onChange={(e) => setEditingLead({...editingLead, linkedinUrl: e.target.value})}
                       className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                       placeholder="https://linkedin.com/in/johnsmith"
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">Company Website</label>
                     <input
                       type="url"
                       value={editingLead.companyWebsite || ''}
                       onChange={(e) => setEditingLead({...editingLead, companyWebsite: e.target.value})}
                       className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                       placeholder="https://techcorp.com"
                     />
                   </div>
                 </div>
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">Use Case</label>
                   <textarea
                     value={editingLead.useCase || ''}
                     onChange={(e) => setEditingLead({...editingLead, useCase: e.target.value})}
                     className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                     rows="3"
                     placeholder="Looking to implement AI in development workflow"
                   />
                 </div>
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">Source</label>
                   <select
                     value={editingLead.source || ''}
                     onChange={(e) => setEditingLead({...editingLead, source: e.target.value})}
                     className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                   >
                     <option value="">Select source</option>
                     <option value="conference">Conference</option>
                     <option value="referral">Referral</option>
                     <option value="website">Website</option>
                     <option value="LinkedIn">LinkedIn</option>
                     <option value="partner">Partner</option>
                     <option value="manual">Manual Entry</option>
                   </select>
                 </div>
                 <div className="flex space-x-3">
                   <button
                     type="button"
                     onClick={() => {
                       setShowEditForm(false);
                       setEditingLead(null);
                     }}
                     className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
                   >
                     Cancel
                   </button>
                   <button
                     type="submit"
                     disabled={isSubmitting}
                     className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
                   >
                     {isSubmitting ? 'Updating...' : 'Update Lead'}
                   </button>
                 </div>
               </form>
             </motion.div>
           </motion.div>
         )}
       </AnimatePresence>

       {/* Lead Detail Modal */}
       <AnimatePresence>
         {showLeadDetail && selectedLead && (
           <motion.div
             initial={{ opacity: 0 }}
             animate={{ opacity: 1 }}
             exit={{ opacity: 0 }}
             className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
             onClick={() => setShowLeadDetail(false)}
           >
             <motion.div
               initial={{ scale: 0.9, opacity: 0 }}
               animate={{ scale: 1, opacity: 1 }}
               exit={{ scale: 0.9, opacity: 0 }}
               className="bg-white rounded-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto"
               onClick={(e) => e.stopPropagation()}
             >
               <div className="flex items-center justify-between mb-6">
                 <h3 className="text-xl font-semibold text-gray-900">Lead Details</h3>
                 <button
                   onClick={() => setShowLeadDetail(false)}
                   className="text-gray-400 hover:text-gray-600 transition-colors"
                 >
                   <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                   </svg>
                 </button>
               </div>

               <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                 {/* Basic Information */}
                 <div className="space-y-4">
                   <div>
                     <h4 className="text-lg font-medium text-gray-900 mb-3">Basic Information</h4>
                     <div className="space-y-3">
                       <div>
                         <label className="block text-sm font-medium text-gray-700">Name</label>
                         <p className="text-gray-900">{selectedLead.name}</p>
                       </div>
                       <div>
                         <label className="block text-sm font-medium text-gray-700">Job Title</label>
                         <p className="text-gray-900">{selectedLead.jobTitle}</p>
                       </div>
                       <div>
                         <label className="block text-sm font-medium text-gray-700">Company</label>
                         <p className="text-gray-900">{selectedLead.company}</p>
                       </div>
                       <div>
                         <label className="block text-sm font-medium text-gray-700">Email</label>
                         <p className="text-gray-900">{selectedLead.email}</p>
                       </div>
                     </div>
                   </div>

                   {/* Contact Information */}
                   <div>
                     <h4 className="text-lg font-medium text-gray-900 mb-3">Contact Information</h4>
                     <div className="space-y-3">
                       {selectedLead.linkedinUrl && (
                         <div>
                           <label className="block text-sm font-medium text-gray-700">LinkedIn</label>
                           <a href={selectedLead.linkedinUrl} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800">
                             {selectedLead.linkedinUrl}
                           </a>
                         </div>
                       )}
                       {selectedLead.companyWebsite && (
                         <div>
                           <label className="block text-sm font-medium text-gray-700">Company Website</label>
                           <a href={selectedLead.companyWebsite} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800">
                             {selectedLead.companyWebsite}
                           </a>
                         </div>
                       )}
                     </div>
                   </div>
                 </div>

                 {/* Lead Analysis */}
                 <div className="space-y-4">
                   <div>
                     <h4 className="text-lg font-medium text-gray-900 mb-3">Lead Analysis</h4>
                     <div className="space-y-3">
                       <div>
                         <label className="block text-sm font-medium text-gray-700">Score</label>
                         <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                           selectedLead.score >= 80 ? 'bg-green-100 text-green-800' :
                           selectedLead.score >= 60 ? 'bg-yellow-100 text-yellow-800' :
                           'bg-red-100 text-red-800'
                         }`}>
                           {selectedLead.score}/100
                         </div>
                       </div>
                       <div>
                         <label className="block text-sm font-medium text-gray-700">Status</label>
                         <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                           selectedLead.status === 'new' ? 'bg-blue-100 text-blue-800' :
                           selectedLead.status === 'analyzing' ? 'bg-yellow-100 text-yellow-800' :
                           selectedLead.status === 'analyzed' ? 'bg-green-100 text-green-800' :
                           selectedLead.status === 'email_drafted' ? 'bg-purple-100 text-purple-800' :
                           'bg-indigo-100 text-indigo-800'
                         }`}>
                           {selectedLead.status.replace('_', ' ').toUpperCase()}
                         </div>
                       </div>
                       <div>
                         <label className="block text-sm font-medium text-gray-700">Industry</label>
                         <p className="text-gray-900">{selectedLead.industry}</p>
                       </div>
                       <div>
                         <label className="block text-sm font-medium text-gray-700">Company Size</label>
                         <p className="text-gray-900">{selectedLead.companySize}</p>
                       </div>
                       <div>
                         <label className="block text-sm font-medium text-gray-700">Source</label>
                         <p className="text-gray-900">{selectedLead.source}</p>
                       </div>
                     </div>
                   </div>

                   {/* Use Case */}
                   {selectedLead.useCase && (
                     <div>
                       <h4 className="text-lg font-medium text-gray-900 mb-3">Use Case</h4>
                       <p className="text-gray-900">{selectedLead.useCase}</p>
                     </div>
                   )}

                   {/* Last Contact */}
                   {selectedLead.lastContact && (
                     <div>
                       <h4 className="text-lg font-medium text-gray-900 mb-3">Last Contact</h4>
                       <p className="text-gray-900">{selectedLead.lastContact}</p>
                     </div>
                   )}
                 </div>
               </div>

                               {/* Action Buttons */}
                <div className="flex justify-end space-x-3 mt-6 pt-6 border-t border-gray-200">
                  <button
                    onClick={() => setShowLeadDetail(false)}
                    className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
                  >
                    Close
                  </button>
                  <button
                    onClick={() => handleGenerateEmail(selectedLead)}
                    disabled={generatingEmail}
                    className="px-4 py-2 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 transition-colors disabled:opacity-50"
                  >
                    {generatingEmail ? (
                      <>
                        <RefreshCw className="w-4 h-4 mr-2 animate-spin inline" />
                        Generating...
                      </>
                    ) : (
                      <>
                        <Mail className="w-4 h-4 mr-2" />
                        Generate Email
                      </>
                    )}
                  </button>
                  <button
                    onClick={() => {
                      handleEditLead(selectedLead);
                      setShowLeadDetail(false);
                    }}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
                  >
                    Edit Lead
                  </button>
                </div>
             </motion.div>
           </motion.div>
         )}
       </AnimatePresence>
     </div>
   );
 };

export default LeadsPage;