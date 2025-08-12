import React, { useState } from 'react';
import { Bot, Sparkles, Target, TrendingUp } from 'lucide-react';
import Header from './components/Header';
import SalesForm from './components/SalesForm';
import ReportDisplay from './components/ReportDisplay';
import Footer from './components/Footer';
import './index.css';

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
      <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2260%22%20height%3D%2260%22%20viewBox%3D%220%200%2060%2060%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%239C92AC%22%20fill-opacity%3D%220.1%22%3E%3Ccircle%20cx%3D%2230%22%20cy%3D%2230%22%20r%3D%221%22/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-20"></div>
      
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
            
            <p className="text-lg text-gray-400 mb-2">
              by Derril Filemon - AI Engineer
            </p>
            
            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Transform your sales process with AI-powered research and personalized pitch generation. Get comprehensive reports in minutes, not hours.
            </p>
          </div>

          {/* Features Section */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            {features.map((feature, index) => (
              <div key={index} className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300">
                <div className="mb-4">{feature.icon}</div>
                <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-gray-300 text-sm">{feature.description}</p>
              </div>
            ))}
          </div>

          {/* Main Content */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
            <SalesForm onGenerateReport={handleGenerateReport} isGenerating={isGenerating} />
            
            {error && (
              <div className="bg-red-500/20 backdrop-blur-sm rounded-2xl p-8 border border-red-500/30">
                <h3 className="text-xl font-bold text-red-400 mb-4">Error</h3>
                <p className="text-red-300">{error}</p>
              </div>
            )}
          </div>

          {/* Report Display */}
          {currentReport && (
            <div className="mb-16">
              <ReportDisplay report={currentReport} />
            </div>
          )}
        </main>
        
        <Footer />
      </div>
    </div>
  );
}

export default App;