'use client'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { X, Target, Zap, Code, Users, TrendingUp } from 'lucide-react'

interface ProjectDescriptionModalProps {
  project: {
    project_name: string
    description: string
    tech_stack: string
    archetype?: string
  }
  isOpen: boolean
  onClose: () => void
}

export function ProjectDescriptionModal({ project, isOpen, onClose }: ProjectDescriptionModalProps) {
  if (!isOpen) return null

  // Generate detailed project description based on project name
  const getProjectDetails = (projectName: string) => {
    const details = {
      goals: [
        "Create a fully functional AI-powered application",
        "Demonstrate modern full-stack development skills",
        "Showcase AI integration and API management",
        "Build a scalable, production-ready solution"
      ],
      features: [
        "User authentication and authorization",
        "Real-time data processing and updates",
        "Responsive design for all devices",
        "Advanced AI/ML integration",
        "Comprehensive error handling",
        "Performance optimization"
      ],
      technical_highlights: [
        "Modern React/Next.js frontend",
        "RESTful API with FastAPI/Express",
        "Database integration (PostgreSQL/MongoDB)",
        "AI/ML model integration",
        "Cloud deployment ready",
        "CI/CD pipeline implementation"
      ],
      business_value: [
        "Automates manual processes",
        "Improves user experience",
        "Reduces operational costs",
        "Provides actionable insights",
        "Scales with business growth"
      ]
    }

    // Customize based on project type
    if (projectName.toLowerCase().includes('chat')) {
      details.goals = [
        "Build an intelligent conversational AI system",
        "Implement natural language processing",
        "Create context-aware responses",
        "Provide seamless user interaction"
      ]
      details.features = [
        "Real-time chat interface",
        "Context memory and conversation history",
        "Multi-language support",
        "Sentiment analysis",
        "Integration with knowledge bases",
        "Voice-to-text capabilities"
      ]
    } else if (projectName.toLowerCase().includes('analysis')) {
      details.goals = [
        "Create comprehensive data analysis tools",
        "Provide actionable business insights",
        "Automate reporting processes",
        "Enable data-driven decision making"
      ]
      details.features = [
        "Advanced data visualization",
        "Real-time analytics dashboard",
        "Custom report generation",
        "Data export capabilities",
        "Trend analysis and forecasting",
        "Automated alerting system"
      ]
    } else if (projectName.toLowerCase().includes('generator')) {
      details.goals = [
        "Automate content creation processes",
        "Generate high-quality outputs",
        "Maintain brand consistency",
        "Scale content production"
      ]
      details.features = [
        "AI-powered content generation",
        "Multiple output formats",
        "Brand voice customization",
        "Quality control mechanisms",
        "Bulk generation capabilities",
        "Template management system"
      ]
    }

    return details
  }

  const projectDetails = getProjectDetails(project.project_name)

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="relative w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
        <Card className="shadow-2xl border-0 bg-white dark:bg-slate-800/95 backdrop-blur-sm">
          <CardHeader className="pb-4">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <CardTitle className="text-2xl font-bold text-gray-900 dark:text-slate-100 flex items-center gap-2">
                  <Target className="w-6 h-6 text-blue-500" />
                  {project.project_name}
                </CardTitle>
                <CardDescription className="text-base text-gray-600 dark:text-slate-300 mt-2">
                  {project.description}
                </CardDescription>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={onClose}
                className="h-8 w-8 p-0 hover:bg-gray-100 dark:hover:bg-slate-700/50"
              >
                <X className="h-4 w-4 text-white" />
              </Button>
            </div>
          </CardHeader>
          
          <CardContent className="space-y-6">
            {/* Project Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Goals */}
              <div className="space-y-3">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 flex items-center gap-2">
                  <Target className="w-5 h-5 text-green-500" />
                  Project Goals
                </h3>
                <ul className="space-y-2">
                  {projectDetails.goals.map((goal, index) => (
                    <li key={index} className="flex items-start gap-2 text-sm text-gray-700 dark:text-slate-300">
                      <div className="w-1.5 h-1.5 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                      {goal}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Features */}
              <div className="space-y-3">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 flex items-center gap-2">
                  <Zap className="w-5 h-5 text-yellow-500" />
                  Key Features
                </h3>
                <ul className="space-y-2">
                  {projectDetails.features.map((feature, index) => (
                    <li key={index} className="flex items-start gap-2 text-sm text-gray-700 dark:text-slate-300">
                      <div className="w-1.5 h-1.5 bg-yellow-500 rounded-full mt-2 flex-shrink-0"></div>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Technical Details */}
            <div className="space-y-3">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 flex items-center gap-2">
                <Code className="w-5 h-5 text-blue-500" />
                Technical Highlights
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {projectDetails.technical_highlights.map((highlight, index) => (
                  <Badge key={index} variant="outline" className="text-xs px-3 py-2 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-700">
                    {highlight}
                  </Badge>
                ))}
              </div>
            </div>

            {/* Business Value */}
            <div className="space-y-3">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-purple-500" />
                Business Value
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {projectDetails.business_value.map((value, index) => (
                  <Badge key={index} variant="outline" className="text-xs px-3 py-2 bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-700">
                    {value}
                  </Badge>
                ))}
              </div>
            </div>

            {/* Tech Stack */}
            <div className="pt-4 border-t border-gray-200 dark:border-slate-600/50">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-700 dark:text-slate-300">Tech Stack:</span>
                <Badge variant="outline" className="text-sm px-4 py-2 text-white bg-slate-600/50 border-slate-500/50">
                  {project.tech_stack}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
