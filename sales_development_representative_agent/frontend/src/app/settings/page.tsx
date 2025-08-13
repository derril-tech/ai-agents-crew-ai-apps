"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Settings, 
  User, 
  Bell, 
  Shield, 
  Database, 
  Zap, 
  Mail, 
  Globe,
  Save,
  RefreshCw,
  Check,
  X
} from 'lucide-react';

const SettingsPage = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [isSaving, setIsSaving] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const [settings, setSettings] = useState({
    profile: {
      name: 'John Doe',
      email: 'john.doe@company.com',
      role: 'Sales Development Representative',
      timezone: 'America/New_York'
    },
    notifications: {
      emailNotifications: true,
      pushNotifications: true,
      leadAlerts: true,
      weeklyReports: false,
      dailyDigest: true
    },
    ai: {
      autoScoring: true,
      emailGeneration: true,
      leadEnrichment: true,
      conversationAnalysis: true,
      aiModel: 'gpt-4'
    },
    integrations: {
      crm: 'Salesforce',
      emailProvider: 'Gmail',
      calendar: 'Google Calendar',
      linkedin: true,
      twitter: false
    },
    security: {
      twoFactorAuth: false,
      sessionTimeout: 30,
      dataRetention: 90,
      apiAccess: true
    }
  });

  const tabs = [
    { id: 'profile', name: 'Profile', icon: User },
    { id: 'notifications', name: 'Notifications', icon: Bell },
    { id: 'ai', name: 'AI Settings', icon: Zap },
    { id: 'integrations', name: 'Integrations', icon: Database },
    { id: 'security', name: 'Security', icon: Shield }
  ];

  const handleSave = async () => {
    setIsSaving(true);
    // Simulate API call
    setTimeout(() => {
      setIsSaving(false);
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    }, 1000);
  };

  const handleSettingChange = (section, key, value) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [key]: value
      }
    }));
  };

  const renderProfileSettings = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
          <input
            type="text"
            value={settings.profile.name}
            onChange={(e) => handleSettingChange('profile', 'name', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
          <input
            type="email"
            value={settings.profile.email}
            onChange={(e) => handleSettingChange('profile', 'email', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Role</label>
          <input
            type="text"
            value={settings.profile.role}
            onChange={(e) => handleSettingChange('profile', 'role', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Timezone</label>
          <select
            value={settings.profile.timezone}
            onChange={(e) => handleSettingChange('profile', 'timezone', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="America/New_York">Eastern Time</option>
            <option value="America/Chicago">Central Time</option>
            <option value="America/Denver">Mountain Time</option>
            <option value="America/Los_Angeles">Pacific Time</option>
            <option value="Europe/London">London</option>
            <option value="Europe/Paris">Paris</option>
          </select>
        </div>
      </div>
    </div>
  );

  const renderNotificationSettings = () => (
    <div className="space-y-6">
      <div className="space-y-4">
        {Object.entries(settings.notifications).map(([key, value]) => (
          <div key={key} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
            <div>
              <h3 className="font-medium text-gray-900 capitalize">
                {key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
              </h3>
              <p className="text-sm text-gray-600">
                {key === 'emailNotifications' && 'Receive notifications via email'}
                {key === 'pushNotifications' && 'Receive push notifications in browser'}
                {key === 'leadAlerts' && 'Get notified when new leads are scored high'}
                {key === 'weeklyReports' && 'Receive weekly performance reports'}
                {key === 'dailyDigest' && 'Get daily summary of activities'}
              </p>
            </div>
            <button
              onClick={() => handleSettingChange('notifications', key, !value)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                value ? 'bg-blue-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  value ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  const renderAISettings = () => (
    <div className="space-y-6">
      <div className="space-y-4">
        {Object.entries(settings.ai).map(([key, value]) => (
          <div key={key} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
            <div>
              <h3 className="font-medium text-gray-900 capitalize">
                {key === 'aiModel' ? 'AI Model' : key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
              </h3>
              <p className="text-sm text-gray-600">
                {key === 'autoScoring' && 'Automatically score leads using AI'}
                {key === 'emailGeneration' && 'Generate personalized emails with AI'}
                {key === 'leadEnrichment' && 'Enrich lead data automatically'}
                {key === 'conversationAnalysis' && 'Analyze email conversations'}
                {key === 'aiModel' && 'Select the AI model for generation'}
              </p>
            </div>
            {key === 'aiModel' ? (
              <select
                value={value}
                onChange={(e) => handleSettingChange('ai', key, e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="gpt-4">GPT-4</option>
                <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                <option value="claude-3">Claude 3</option>
              </select>
            ) : (
              <button
                onClick={() => handleSettingChange('ai', key, !value)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  value ? 'bg-blue-600' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    value ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );

  const renderIntegrationSettings = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">CRM System</label>
          <select
            value={settings.integrations.crm}
            onChange={(e) => handleSettingChange('integrations', 'crm', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="Salesforce">Salesforce</option>
            <option value="HubSpot">HubSpot</option>
            <option value="Pipedrive">Pipedrive</option>
            <option value="Zoho">Zoho CRM</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Email Provider</label>
          <select
            value={settings.integrations.emailProvider}
            onChange={(e) => handleSettingChange('integrations', 'emailProvider', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="Gmail">Gmail</option>
            <option value="Outlook">Outlook</option>
            <option value="Yahoo">Yahoo</option>
            <option value="Custom SMTP">Custom SMTP</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Calendar</label>
          <select
            value={settings.integrations.calendar}
            onChange={(e) => handleSettingChange('integrations', 'calendar', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="Google Calendar">Google Calendar</option>
            <option value="Outlook Calendar">Outlook Calendar</option>
            <option value="Apple Calendar">Apple Calendar</option>
          </select>
        </div>
      </div>
      
      <div className="space-y-4">
        <h3 className="text-lg font-medium text-gray-900">Social Media Integrations</h3>
        {Object.entries(settings.integrations).filter(([key]) => ['linkedin', 'twitter'].includes(key)).map(([key, value]) => (
          <div key={key} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                key === 'linkedin' ? 'bg-blue-600' : 'bg-blue-400'
              }`}>
                <Globe className="w-4 h-4 text-white" />
              </div>
              <div>
                <h3 className="font-medium text-gray-900 capitalize">{key}</h3>
                <p className="text-sm text-gray-600">Connect your {key} account</p>
              </div>
            </div>
            <button
              onClick={() => handleSettingChange('integrations', key, !value)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                value ? 'bg-blue-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  value ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  const renderSecuritySettings = () => (
    <div className="space-y-6">
      <div className="space-y-4">
        <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
          <div>
            <h3 className="font-medium text-gray-900">Two-Factor Authentication</h3>
            <p className="text-sm text-gray-600">Add an extra layer of security to your account</p>
          </div>
          <button
            onClick={() => handleSettingChange('security', 'twoFactorAuth', !settings.security.twoFactorAuth)}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
              settings.security.twoFactorAuth ? 'bg-blue-600' : 'bg-gray-200'
            }`}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                settings.security.twoFactorAuth ? 'translate-x-6' : 'translate-x-1'
              }`}
            />
          </button>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Session Timeout (minutes)</label>
          <select
            value={settings.security.sessionTimeout}
            onChange={(e) => handleSettingChange('security', 'sessionTimeout', parseInt(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value={15}>15 minutes</option>
            <option value={30}>30 minutes</option>
            <option value={60}>1 hour</option>
            <option value={120}>2 hours</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Data Retention (days)</label>
          <select
            value={settings.security.dataRetention}
            onChange={(e) => handleSettingChange('security', 'dataRetention', parseInt(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value={30}>30 days</option>
            <option value={90}>90 days</option>
            <option value={180}>180 days</option>
            <option value={365}>1 year</option>
          </select>
        </div>
        
        <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
          <div>
            <h3 className="font-medium text-gray-900">API Access</h3>
            <p className="text-sm text-gray-600">Allow API access for integrations</p>
          </div>
          <button
            onClick={() => handleSettingChange('security', 'apiAccess', !settings.security.apiAccess)}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
              settings.security.apiAccess ? 'bg-blue-600' : 'bg-gray-200'
            }`}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                settings.security.apiAccess ? 'translate-x-6' : 'translate-x-1'
              }`}
            />
          </button>
        </div>
      </div>
    </div>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'profile':
        return renderProfileSettings();
      case 'notifications':
        return renderNotificationSettings();
      case 'ai':
        return renderAISettings();
      case 'integrations':
        return renderIntegrationSettings();
      case 'security':
        return renderSecuritySettings();
      default:
        return renderProfileSettings();
    }
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
            Settings
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Configure your SDR Assistant preferences and integrations
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <button
            onClick={handleSave}
            disabled={isSaving}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center disabled:opacity-50"
          >
            {isSaving ? (
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <Save className="w-4 h-4 mr-2" />
            )}
            {isSaving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </motion.div>

      {/* Success Message */}
      {showSuccess && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-center space-x-3"
        >
          <Check className="w-5 h-5 text-green-600" />
          <span className="text-green-800 font-medium">Settings saved successfully!</span>
        </motion.div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Tabs */}
        <div className="lg:col-span-1">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-4"
          >
            <nav className="space-y-2">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-100 text-blue-700 border border-blue-200'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <tab.icon className="w-5 h-5" />
                  <span className="font-medium">{tab.name}</span>
                </button>
              ))}
            </nav>
          </motion.div>
        </div>

        {/* Content */}
        <div className="lg:col-span-3">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
          >
            <h2 className="text-xl font-semibold text-gray-900 mb-6 capitalize">
              {activeTab === 'ai' ? 'AI Settings' : activeTab} Settings
            </h2>
            {renderContent()}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
