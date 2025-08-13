"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Zap, 
  Brain, 
  MessageSquare, 
  Target, 
  TrendingUp, 
  Users, 
  Mail, 
  Search,
  Play,
  Settings,
  Download,
  Copy
} from 'lucide-react';

const AIToolsPage = () => {
  const [activeTool, setActiveTool] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedContent, setGeneratedContent] = useState('');

  const tools = [
    {
      id: 'email-generator',
      name: 'AI Email Generator',
      description: 'Generate personalized cold emails based on lead data',
      icon: Mail,
      color: 'blue',
      features: ['Personalized content', 'Multiple templates', 'A/B testing suggestions']
    },
    {
      id: 'lead-scorer',
      name: 'Lead Scoring AI',
      description: 'Automatically score leads based on multiple criteria',
      icon: Target,
      color: 'green',
      features: ['Real-time scoring', 'Custom criteria', 'Priority ranking']
    },
    {
      id: 'conversation-analyzer',
      name: 'Conversation Analyzer',
      description: 'Analyze email conversations and extract insights',
      icon: MessageSquare,
      color: 'purple',
      features: ['Sentiment analysis', 'Engagement metrics', 'Response optimization']
    },
    {
      id: 'market-researcher',
      name: 'Market Research AI',
      description: 'Research companies and industries automatically',
      icon: Search,
      color: 'orange',
      features: ['Company insights', 'Industry trends', 'Competitive analysis']
    },
    {
      id: 'pitch-optimizer',
      name: 'Pitch Optimizer',
      description: 'Optimize your sales pitches for better conversion',
      icon: TrendingUp,
      color: 'red',
      features: ['Performance tracking', 'A/B testing', 'Conversion optimization']
    },
    {
      id: 'lead-enrichment',
      name: 'Lead Enrichment',
      description: 'Automatically enrich lead data with additional information',
      icon: Users,
      color: 'indigo',
      features: ['Contact details', 'Social profiles', 'Company information']
    }
  ];

  const handleToolClick = (tool) => {
    setActiveTool(tool);
    setGeneratedContent('');
  };

  const handleGenerate = async () => {
    if (!activeTool) return;
    
    setIsGenerating(true);
    
    // Simulate AI generation
    setTimeout(() => {
      const mockContent = {
        'email-generator': `Subject: AI-Powered Sales Development for ${activeTool.name}

Hi [Lead Name],

I noticed that [Company Name] is expanding their [department] team, and I wanted to reach out about how our AI-powered sales development platform could help streamline your lead generation process.

Based on your company's growth trajectory, I believe we could help you:
• Increase lead quality by 40%
• Reduce response time by 60%
• Improve conversion rates by 25%

Would you be interested in a 15-minute call to discuss how we've helped similar companies achieve these results?

Best regards,
[Your Name]`,
        'lead-scorer': `Lead Score: 85/100

Scoring Breakdown:
• Company Size: 25/25 (Enterprise)
• Industry Match: 20/25 (Technology)
• Decision Maker: 20/25 (VP Level)
• Engagement History: 20/25 (Active)

Recommendation: High Priority - Immediate follow-up recommended`,
        'conversation-analyzer': `Conversation Analysis Results:

Sentiment: Positive (0.8/1.0)
Engagement Level: High
Key Topics: AI implementation, cost savings, ROI
Response Time: 2.3 hours (Excellent)
Next Best Action: Schedule demo call

Optimization Suggestions:
• Mention specific ROI metrics
• Include case study from similar industry
• Follow up within 24 hours`,
        'market-researcher': `Company Research: TechCorp Inc.

Industry: Software Development
Size: 500-1000 employees
Revenue: $50M-$100M
Growth Rate: 25% YoY
Recent News: Series B funding round
Key Decision Makers: CTO, VP Engineering

Market Position: Growing rapidly in AI/ML space
Competitive Advantages: Strong technical team, innovative products`,
        'pitch-optimizer': `Pitch Performance Analysis:

Current Conversion Rate: 12%
Target Conversion Rate: 18%
Gap Analysis: Need stronger value proposition

Optimized Pitch Elements:
• Lead with specific pain point
• Include social proof (case studies)
• Clear call-to-action
• Follow-up sequence

Expected Improvement: +6% conversion rate`,
        'lead-enrichment': `Enriched Lead Data:

Contact Information:
• Email: john.smith@techcorp.com
• Phone: +1 (555) 123-4567
• LinkedIn: linkedin.com/in/johnsmith

Company Information:
• Industry: Technology
• Size: 500-1000 employees
• Revenue: $50M-$100M
• Location: San Francisco, CA

Social Profiles:
• Twitter: @johnsmith_tech
• GitHub: github.com/johnsmith`
      };
      
      setGeneratedContent(mockContent[activeTool.id] || 'Content generated successfully!');
      setIsGenerating(false);
    }, 2000);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedContent);
    alert('Content copied to clipboard!');
  };

  const handleDownload = () => {
    const blob = new Blob([generatedContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${activeTool?.name.replace(/\s+/g, '_').toLowerCase()}_${new Date().toISOString().split('T')[0]}.txt`;
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
            AI Tools
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Leverage AI to supercharge your sales development process
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <Brain className="w-4 h-4" />
            <span>Powered by Advanced AI</span>
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Tools List */}
        <div className="lg:col-span-1">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
          >
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Available Tools</h2>
            <div className="space-y-3">
              {tools.map((tool, index) => (
                <motion.button
                  key={tool.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  onClick={() => handleToolClick(tool)}
                  className={`w-full p-4 rounded-lg border transition-all duration-200 text-left ${
                    activeTool?.id === tool.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div className={`p-2 rounded-lg ${
                      tool.color === 'blue' ? 'bg-blue-100' :
                      tool.color === 'green' ? 'bg-green-100' :
                      tool.color === 'purple' ? 'bg-purple-100' :
                      tool.color === 'orange' ? 'bg-orange-100' :
                      tool.color === 'red' ? 'bg-red-100' : 'bg-indigo-100'
                    }`}>
                      <tool.icon className={`w-5 h-5 ${
                        tool.color === 'blue' ? 'text-blue-600' :
                        tool.color === 'green' ? 'text-green-600' :
                        tool.color === 'purple' ? 'text-purple-600' :
                        tool.color === 'orange' ? 'text-orange-600' :
                        tool.color === 'red' ? 'text-red-600' : 'text-indigo-600'
                      }`} />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900">{tool.name}</h3>
                      <p className="text-sm text-gray-600">{tool.description}</p>
                    </div>
                  </div>
                </motion.button>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Tool Interface */}
        <div className="lg:col-span-2">
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
          >
            {activeTool ? (
              <div className="space-y-6">
                {/* Tool Header */}
                <div className="flex items-center space-x-3">
                  <div className={`p-3 rounded-lg ${
                    activeTool.color === 'blue' ? 'bg-blue-100' :
                    activeTool.color === 'green' ? 'bg-green-100' :
                    activeTool.color === 'purple' ? 'bg-purple-100' :
                    activeTool.color === 'orange' ? 'bg-orange-100' :
                    activeTool.color === 'red' ? 'bg-red-100' : 'bg-indigo-100'
                  }`}>
                    <activeTool.icon className={`w-6 h-6 ${
                      activeTool.color === 'blue' ? 'text-blue-600' :
                      activeTool.color === 'green' ? 'text-green-600' :
                      activeTool.color === 'purple' ? 'text-purple-600' :
                      activeTool.color === 'orange' ? 'text-orange-600' :
                      activeTool.color === 'red' ? 'text-red-600' : 'text-indigo-600'
                    }`} />
                  </div>
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900">{activeTool.name}</h2>
                    <p className="text-gray-600">{activeTool.description}</p>
                  </div>
                </div>

                {/* Features */}
                <div>
                  <h3 className="text-sm font-medium text-gray-700 mb-2">Features:</h3>
                  <div className="flex flex-wrap gap-2">
                    {activeTool.features.map((feature, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full"
                      >
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Generate Button */}
                <div className="flex space-x-3">
                  <button
                    onClick={handleGenerate}
                    disabled={isGenerating}
                    className="flex-1 bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center justify-center disabled:opacity-50"
                  >
                    {isGenerating ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Generating...
                      </>
                    ) : (
                      <>
                        <Zap className="w-4 h-4 mr-2" />
                        Generate with AI
                      </>
                    )}
                  </button>
                  <button className="px-4 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors">
                    <Settings className="w-4 h-4" />
                  </button>
                </div>

                {/* Generated Content */}
                {generatedContent && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-4"
                  >
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-medium text-gray-900">Generated Content</h3>
                      <div className="flex space-x-2">
                        <button
                          onClick={handleCopy}
                          className="px-3 py-1 text-sm border border-gray-300 text-gray-700 rounded hover:bg-gray-50 transition-colors flex items-center"
                        >
                          <Copy className="w-3 h-3 mr-1" />
                          Copy
                        </button>
                        <button
                          onClick={handleDownload}
                          className="px-3 py-1 text-sm border border-gray-300 text-gray-700 rounded hover:bg-gray-50 transition-colors flex items-center"
                        >
                          <Download className="w-3 h-3 mr-1" />
                          Download
                        </button>
                      </div>
                    </div>
                    <div className="p-4 bg-gray-50 rounded-lg border">
                      <pre className="whitespace-pre-wrap text-sm text-gray-900 font-mono">
                        {generatedContent}
                      </pre>
                    </div>
                  </motion.div>
                )}
              </div>
            ) : (
              <div className="text-center py-12">
                <Zap className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Select an AI Tool</h3>
                <p className="text-gray-600">
                  Choose a tool from the left panel to get started with AI-powered sales development.
                </p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default AIToolsPage;
