'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { TodoModal } from '@/components/todo-modal'
import { todoManager } from '@/lib/todo-manager'
import { agentSimulator } from '@/lib/agent-simulator'
import { 
  CheckCircle, 
  Clock, 
  AlertCircle, 
  Play, 
  Target, 
  TrendingUp,
  Zap,
  Users,
  Code,
  Database,
  Globe,
  Shield,
  Bot,
  Square
} from 'lucide-react'

interface Project {
  project_name: string
  description: string
  tech_stack: string
  why_impressive: string
  status?: 'complete' | 'in_progress' | 'not_started' | 'failed'
  progress?: number
  files?: string[]
  activeAgents?: string[]
}

interface Stats {
  total: number
  complete: number
  in_progress: number
  failed: number
  not_started: number
}

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([])
  const [stats, setStats] = useState<Stats>({
    total: 0,
    complete: 0,
    in_progress: 0,
    failed: 0,
    not_started: 0
  })
  const [showAllProjects, setShowAllProjects] = useState(false)
  const [selectedProject, setSelectedProject] = useState<Project | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isSimulationRunning, setIsSimulationRunning] = useState(false)

  // Helper function for safer API calls
  async function getJson(url: string) {
    const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
    if (!res.ok) {
      const text = await res.text().catch(() => '');
      throw new Error(`Fetch failed: ${res.status} ${res.statusText} – ${text || 'no body'}`);
    }
    return res.json();
  }

  useEffect(() => {
    console.log('🚀 Dashboard useEffect started')
    
    // Load projects from backend server
    const loadProjects = async () => {
      try {
        const data = await getJson('/api/projects');
        console.log('📋 Projects loaded:', data)
        setProjects(data)
        calculateStats(data)
      } catch (error) {
        console.error('❌ Failed to load /api/projects:', error)
        // Fallback to sample data
        const sampleProjects = [
          {
            project_name: "AI-Powered Code Review & Refactoring Assistant",
            description: "Automated code analysis, security vulnerability detection, performance optimization suggestions",
            tech_stack: "Python, FastAPI, React, OpenAI/Claude API",
            why_impressive: "Shows full-stack development, AI integration, and understanding of software engineering best practices",
            status: "not_started" as const,
            progress: 0
          },
          {
            project_name: "Intelligent Document Processing & Knowledge Base",
            description: "Multi-format document ingestion, semantic search, automated summarization, Q&A system",
            tech_stack: "Python, LangChain, Vector DB, React, FastAPI",
            why_impressive: "Demonstrates RAG architecture, vector embeddings, and enterprise-level document management",
            status: "not_started" as const,
            progress: 0
          }
        ]
        setProjects(sampleProjects)
        calculateStats(sampleProjects)
      }
    }
    
    loadProjects()

        // Set up real-time refresh for pipeline data
    const refreshInterval = setInterval(async () => {
      try {
        const response = await getJson(`/api/pipeline?v=${Date.now()}`);
        const pipelineData = response.items || response // Handle both new and old format
        console.log('🔄 Pipeline data refreshed:', pipelineData)
        
        // Update projects with pipeline data
        setProjects(prevProjects => {
          console.log('[DEBUG] Pipeline data keys:', Object.keys(pipelineData))
          
          const updatedProjects: Project[] = prevProjects.map(project => {
            const projectId = project.project_name.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9\s-]+/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '')
            const pipelineProject = pipelineData[projectId]
            
            // Debug for the specific project
            if (project.project_name === "AI-Powered Code Review & Refactoring Assistant") {
              console.log(`[DEBUG] Looking for project ID: "${projectId}"`)
              console.log(`[DEBUG] Found pipeline data:`, pipelineProject)
              console.log(`[DEBUG] Pipeline data keys:`, Object.keys(pipelineData))
            }
            
            if (pipelineProject) {
              const updatedProject = {
                ...project,
                progress: pipelineProject.progress || 0,
                status: (pipelineProject.progress === 100 ? 'complete' : 
                        pipelineProject.progress > 0 ? 'in_progress' : 'not_started') as 'complete' | 'in_progress' | 'not_started' | 'failed',
                activeAgents: pipelineProject.activeAgents || []
              }
              
              // Debug for the specific project
              if (project.project_name === "AI-Powered Code Review & Refactoring Assistant") {
                console.log(`[DEBUG] Updated project:`, updatedProject)
              }
              
              return updatedProject
            }
            return project
          })
          
          calculateStats(updatedProjects)
          return updatedProjects
        })
      } catch (error) {
        console.error('❌ /api/pipeline failed:', error)
      }
    }, 2000) // Refresh every 2 seconds

    return () => clearInterval(refreshInterval)
  }, [])

  const calculateStats = (projectList: Project[]) => {
    const newStats = {
      total: projectList.length,
      complete: projectList.filter(p => p.progress === 100).length,
      in_progress: projectList.filter(p => p.progress && p.progress > 0 && p.progress < 100).length,
      failed: projectList.filter(p => p.status === 'failed').length,
      not_started: projectList.filter(p => !p.progress || p.progress === 0).length
    }
    setStats(newStats)
  }

  const getStatusIcon = (project: Project) => {
    if (project.progress === 100) {
      return <CheckCircle className="w-4 h-4 text-green-500" />
    } else if (project.progress && project.progress > 0) {
      return <Clock className="w-4 h-4 text-yellow-500" />
    } else if (project.status === 'failed') {
      return <AlertCircle className="w-4 h-4 text-red-500" />
    } else {
      return <Play className="w-4 h-4 text-gray-500" />
    }
  }

  const getStatusBadge = (project: Project) => {
    const hasActiveAgents = project.activeAgents && project.activeAgents.length > 0
    
    if (project.progress === 100) {
      return <Badge variant="outline" className="text-green-600 bg-green-50 border-green-200">Complete</Badge>
    } else if (project.progress && project.progress > 0) {
      return (
        <Badge 
          variant="outline" 
          className={`text-blue-600 bg-blue-50 border-blue-200 ${hasActiveAgents ? 'animate-pulse font-bold' : ''}`}
          style={hasActiveAgents ? {
            animation: 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            backgroundColor: '#dbeafe',
            borderColor: '#3b82f6',
            color: '#1d4ed8'
          } : {}}
        >
          {hasActiveAgents ? '[WORKING] Active Agent' : 'In Progress'}
        </Badge>
      )
    } else if (project.status === 'failed') {
      return <Badge variant="outline" className="text-red-600 bg-red-50 border-red-200">Failed</Badge>
    } else {
      return <Badge variant="outline" className="text-gray-600 bg-gray-50 border-gray-200">Not Started</Badge>
    }
  }

  const overallProgress = stats.total > 0 ? Math.round((stats.complete / stats.total) * 100) : 0

  const handleProjectClick = (project: Project) => {
    setSelectedProject(project)
    setIsModalOpen(true)
  }

  const handleModalClose = () => {
    setIsModalOpen(false)
    setSelectedProject(null)
  }

  const handleProgressUpdate = (projectId: string, progress: number) => {
    setProjects(prevProjects => {
      const updatedProjects = prevProjects.map(project => {
                 const projectIdMatch = project.project_name.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9\s-]+/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '')
        if (projectIdMatch === projectId) {
          return { ...project, progress }
        }
        return project
      })
      
      // Recalculate stats with updated projects
      calculateStats(updatedProjects)
      return updatedProjects
    })
  }

  const handleStartSimulation = async () => {
    console.log('🚀 Starting real pipeline execution...')
    setIsSimulationRunning(true)
    
    try {
      const res = await fetch('/api/run-pipeline', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' } 
      });
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      const result = await res.json();
      if (!result.success) throw new Error(result.error || 'pipeline failed');
      console.log('🎉 Pipeline executed successfully!')
    } catch (error) {
      console.error('❌ /api/run-pipeline failed:', error)
      setIsSimulationRunning(false)
    }
  }

  const handleStopSimulation = async () => {
    console.log('🛑 Stopping simulation and clearing active agents...')
    setIsSimulationRunning(false)
    
    try {
      // Call backend to clear pipeline data
      const res = await fetch('/api/stop-pipeline', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' } 
      });
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      const result = await res.json();
      if (!result.success) throw new Error(result.error || 'stop pipeline failed');
      console.log('✅ Pipeline stopped and active agents cleared')
    } catch (error) {
      console.error('❌ /api/stop-pipeline failed:', error)
    }
    
    // Clear all active agents from projects immediately
    setProjects(prevProjects => {
      const updatedProjects = prevProjects.map(project => ({
        ...project,
        activeAgents: []
      }))
      calculateStats(updatedProjects)
      return updatedProjects
    })
  }

  const handleResetSimulation = () => {
    agentSimulator.resetAllProjects()
    // Force re-render
    setProjects([...projects])
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 gradient-text">
            60 AI Apps Pipeline
          </h1>
          <p className="text-xl text-muted-foreground mb-2">Progress Dashboard</p>
          <p className="text-sm text-muted-foreground">
            Building the future, one AI app at a time
          </p>
        </div>

        {/* Agent Simulation Controls */}
        <div className="mb-8 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-700">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Bot className="h-5 w-5 text-blue-600" />
              <h3 className="font-semibold text-blue-900 dark:text-blue-100">Agent Simulation</h3>
              <span className="text-sm text-blue-600 dark:text-blue-300">
                {isSimulationRunning ? '🤖 Running' : '⏸️ Stopped'}
              </span>
            </div>
            <div className="flex items-center gap-2">
              {!isSimulationRunning ? (
                <button
                  onClick={handleStartSimulation}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
                >
                  <Play className="h-4 w-4" />
                  Start Simulation
                </button>
              ) : (
                <button
                  onClick={handleStopSimulation}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2"
                >
                  <Square className="h-4 w-4" />
                  Stop Simulation
                </button>
              )}
              <button
                onClick={handleResetSimulation}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                Reset All
              </button>
            </div>
          </div>
          <p className="text-sm text-blue-700 dark:text-blue-300 mt-2">
            Watch agents work on projects in real-time! Projects with active agents will show blinking animations.
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="card-hover">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Projects</CardTitle>
              <Target className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total}</div>
              <p className="text-xs text-muted-foreground">
                All AI applications
              </p>
            </CardContent>
          </Card>

          <Card className="card-hover">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Completed</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{stats.complete}</div>
              <p className="text-xs text-muted-foreground">
                Ready to deploy
              </p>
            </CardContent>
          </Card>

          <Card className="card-hover">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">In Progress</CardTitle>
              <Clock className="h-4 w-4 text-yellow-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">{stats.in_progress}</div>
              <p className="text-xs text-muted-foreground">
                Currently building
              </p>
            </CardContent>
          </Card>

          <Card className="card-hover">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Not Started</CardTitle>
              <Play className="h-4 w-4 text-gray-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-600">{stats.not_started}</div>
              <p className="text-xs text-muted-foreground">
                Ready to begin
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Overall Progress */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Overall Progress
            </CardTitle>
            <CardDescription>
              {stats.complete} of {stats.total} projects completed
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Progress</span>
                <span className="font-medium">{overallProgress}%</span>
              </div>
              <Progress value={overallProgress} className="h-3" />
            </div>
          </CardContent>
        </Card>

        {/* Projects Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.slice(0, showAllProjects ? projects.length : 12).map((project, index) => {
                         const projectId = project.project_name.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9\s-]+/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '')
            const hasActiveAgents = project.activeAgents && project.activeAgents.length > 0
            
            // Debug logging
            if (project.project_name === "AI-Powered Code Review & Refactoring Assistant") {
              console.log(`[DEBUG] Project: ${project.project_name}`)
              console.log(`[DEBUG] activeAgents:`, project.activeAgents)
              console.log(`[DEBUG] hasActiveAgents:`, hasActiveAgents)
              console.log(`[DEBUG] progress:`, project.progress)
              console.log(`[DEBUG] status:`, project.status)
            }
            
            return (
            <Card 
              key={index} 
              className={`card-hover cursor-pointer ${hasActiveAgents ? 'animate-pulse border-red-300 shadow-lg shadow-red-200 bg-red-50' : ''}`}
              style={hasActiveAgents ? {
                animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                borderWidth: '2px',
                borderColor: '#ef4444',
                backgroundColor: '#fef2f2 !important'
              } : {}}
              onClick={() => handleProjectClick(project)}
            >
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg line-clamp-2">{project.project_name}</CardTitle>
                    <CardDescription className="line-clamp-2 mt-2">
                      {project.description}
                    </CardDescription>
                  </div>
                  <div className="ml-2">
                    {getStatusIcon(project)}
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center gap-2">
                  {getStatusBadge(project)}
                  <span className="text-xs text-muted-foreground">
                    {project.progress || 0}% complete
                  </span>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <Code className="h-3 w-3" />
                    <span className="line-clamp-1">{project.tech_stack}</span>
                  </div>
                </div>

                <Progress value={project.progress || 0} className="h-2" />
              </CardContent>
            </Card>
            )
          })}
        </div>

        {/* Show More/Less Button */}
        {projects.length > 12 && (
          <div className="text-center mt-8">
            <button 
              onClick={() => setShowAllProjects(!showAllProjects)}
              className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
            >
              {showAllProjects ? (
                <>
                  <Zap className="h-4 w-4" />
                  Show First 12 Projects
                </>
              ) : (
                <>
                  <Zap className="h-4 w-4" />
                  View All {projects.length} Projects
                </>
              )}
            </button>
          </div>
        )}

        {/* Todo Modal */}
        {selectedProject && (
          <TodoModal
            project={selectedProject}
            isOpen={isModalOpen}
            onClose={handleModalClose}
            onProgressUpdate={(progress) => {
                             const projectId = selectedProject.project_name.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9\s-]+/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '')
              handleProgressUpdate(projectId, progress)
            }}
          />
        )}
      </div>
    </div>
  )
}
