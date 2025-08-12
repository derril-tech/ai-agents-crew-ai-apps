import React, { useState, useEffect } from 'react';
import { Bot, Sparkles, Target, TrendingUp, Users, Zap } from 'lucide-react';
import Header from './components/Header';
import SalesForm from './components/SalesForm';
import ReportDisplay from './components/ReportDisplay';
import Footer from './components/Footer';
import './styles/globals.css';

function App() {
  const [currentReport, setCurrentReport] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateReport = async (person, company) => {
    setIsGenerating(true);
    setError(null);
    
    try {
      const response = await fetch('/api/generate-sales-pitch', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ person, company }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        setCurrentReport(data);
      } else {
        setError(data.error || 'Failed to generate report');
      }
    } catch (err) {
      setError('Network error: Could not connect to the server');
    } finally {
      setIsGenerating(false);
    }
  };

  const features = [
    {
      icon: <Bot className="w-8 h-8 text-blue-500" />,
      title: "AI-Powered Research",
      description: "Advanced multi-agent system conducts comprehensive company and executive research"
    },
    {
      icon: <Target className="w-8 h-8 text-green-500" />,
      title: "Personalized Pitches",
      description: "Tailored sales strategies based on specific company needs and executive profiles"
    },
    {
      icon: <TrendingUp className="w-8 h-8 text-purple-500" />,
      title: "Real-time Intelligence",
      description: "Live web research provides up-to-date company insights and market intelligence"
    },
    {
      icon: <Sparkles className="w-8 h-8 text-yellow-500" />,
      title: "Professional Reports",
      description: "Structured markdown reports ready for immediate use in sales meetings"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%239C92AC" fill-opacity="0.1"%3E%3Ccircle cx="30" cy="30" r="1"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-20"></div>
      
      <div className="relative z-10">
        <Header />
        
        <main className="container mx-auto px-4 py-8">
          {/* Hero Section */}
          <div className="text-center mb-16">
            <div className="flex justify-center mb-6">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full blur-lg opacity-30 animate-pulse"></div>
                <Bot className="relative w-20 h-20 text-white" />
              </div>
            </div>
            
            <h1 className="text-5xl font-bold text-white mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              AI Sales Pitch Assistant
            </h1>
            
            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Transform your sales process with AI-powered research and personalized pitch