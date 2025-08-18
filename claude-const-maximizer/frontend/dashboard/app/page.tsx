'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { TodoModal } from '@/components/todo-modal'
import FinalReportModal from '@/components/final-report-modal'
import { todoManager } from '@/lib/todo-manager'
import { agentSimulator } from '@/lib/agent-simulator'
import { pipelineSimulator } from '@/lib/pipeline-simulator'
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
  RefreshCw
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
  const [completionReportProject, setCompletionReportProject] = useState<Project | null>(null)
  const [isCompletionModalOpen, setIsCompletionModalOpen] = useState(false)

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

        // Set up real-time refresh for pipeline data from real backend
    const refreshInterval = setInterval(async () => {
      try {
        let backendData: Record<string, any> = {}
        let localData: Record<string, any> = {}
        
        // Try to read from real backend first
        try {
          const res = await fetch('http://localhost:8001/api/pipeline-status')
          if (res.ok) {
            backendData = await res.json()
            console.log('🔄 Backend data:', backendData)
          } else {
            throw new Error('Backend not available')
          }
        } catch (backendError) {
          console.log('🔄 Backend not available, using local data only')
        }
        
        // Always read local data as fallback
        const stored = localStorage.getItem('pipeline-data')
        localData = stored ? JSON.parse(stored) : {}
        console.log('🔄 Local data:', localData)
        
        // Merge: most recent wins per projectId
        const merged: Record<string, any> = { ...backendData }
        for (const [pid, local] of Object.entries(localData)) {
          const remote = backendData[pid]
          const newerLocal =
            !remote ||
            new Date(local.lastUpdated || 0).getTime() > new Date(remote.lastUpdated || 0).getTime() ||
            ((remote.progress ?? 0) === 0 && (local.progress ?? 0) > 0) // prefer moving local over idle remote
          if (newerLocal) merged[pid] = local
        }
        
        console.log('🔄 Merged data:', merged)
        
        // Update projects with merged pipeline data
        setProjects(prevProjects => {
          const updatedProjects: Project[] = prevProjects.map(project => {
            const projectId = project.project_name.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9\s-]+/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '')
            const pipelineProject = merged[projectId]
            
            if (pipelineProject) {
              const updatedProject = {
                ...project,
                progress: pipelineProject.progress || 0,
                status: (pipelineProject.progress === 100 ? 'complete' : 
                        pipelineProject.progress > 0 ? 'in_progress' : 'not_started') as 'complete' | 'in_progress' | 'not_started' | 'failed',
                activeAgents: pipelineProject.activeAgents || []
              }
              
              // Check if project just completed
              const wasInProgress = project.progress && project.progress > 0 && project.progress < 100
              const justCompleted = updatedProject.progress === 100 && wasInProgress
              
              if (justCompleted) {
                console.log(`🎉 Project completed: ${project.project_name}`)
                setCompletionReportProject(updatedProject)
                setIsCompletionModalOpen(true)
              }
              
              return updatedProject
            }
            return project
          })
          
          calculateStats(updatedProjects)
          return updatedProjects
        })
      } catch (error) {
        console.error('❌ Failed to load pipeline data:', error)
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
    } else if (project.status === 'failed') {
      return <Badge variant="outline" className="text-red-600 bg-red-50 border-red-200">Failed</Badge>
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
          {hasActiveAgents ? `[WORKING] ${project.activeAgents?.[0] || 'Agent'}` : 'In Progress'}
        </Badge>
      )
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



  const handleRunSingleProject = async (project: Project) => {
    console.log(`🚀 Starting pipeline for: ${project.project_name}`)
    
    const projectId = project.project_name.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9\s-]+/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '')
    
    try {
      // Try to start the real CrewAI backend first
      const res = await fetch('http://localhost:8001/api/run-crewai-project', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectId,
          projectName: project.project_name
        })
      })
      
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
      const result = await res.json()
      if (!result.success) throw new Error(result.error || 'start failed')
      
      console.log(`🎉 Real CrewAI pipeline started for ${project.project_name}!`)
      
      // Give backend a moment, then check if it's actually updating
      setTimeout(async () => {
        const stored = JSON.parse(localStorage.getItem('pipeline-data') || '{}')
        const p = stored[projectId]
        const stuck = !p || (p.progress ?? 0) === 0
        
        if (stuck) {
          console.log('🔄 Backend not updating, starting simulator...')
          await pipelineSimulator.startSimulationForProject(projectId, project.project_name)
        }
      }, 1500)
      
    } catch (error) {
      console.error(`❌ Failed to start real pipeline for ${project.project_name}:`, error)
      // Fallback to simulator for testing
      console.log('🔄 Falling back to simulator...')
      await pipelineSimulator.startSimulationForProject(projectId, project.project_name)
    }
  }

  const handleStopProject = async (project: Project) => {
    console.log(`🛑 Stopping pipeline for: ${project.project_name}`)
    
    const projectId = project.project_name.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9\s-]+/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '')
    
    try {
      // Stop the specific project's CrewAI backend
      const res = await fetch('http://localhost:8001/api/stop-project', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectId,
          projectName: project.project_name
        })
      })
      
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
      const result = await res.json()
      if (!result.success) throw new Error(result.error || 'stop failed')
      
      console.log(`🛑 Real CrewAI pipeline stopped for ${project.project_name}!`)
    } catch (error) {
      console.error(`❌ Failed to stop real pipeline for ${project.project_name}:`, error)
      
      // If specific project stop fails, try the general stop
      try {
        console.log('🔄 Trying general stop...')
        const res = await fetch('http://localhost:8001/api/stop-pipeline', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({})
        })
        
        if (res.ok) {
          const result = await res.json()
          console.log(`🛑 General pipeline stop successful: ${result.message}`)
        }
      } catch (generalError) {
        console.error('❌ General stop also failed:', generalError)
        // Fallback to simulator for testing
        console.log('🔄 Falling back to simulator...')
        await pipelineSimulator.stopSimulation()
      }
    }
    
    // Always reset the project state in localStorage to stop the UI
    try {
      const stored = localStorage.getItem('pipeline-data')
      const pipelineData = stored ? JSON.parse(stored) : {}
      
      // Reset the specific project
      if (pipelineData[projectId]) {
        pipelineData[projectId] = {
          ...pipelineData[projectId],
          progress: 0,
          activeAgents: [],
          status: 'stopped',
          currentTask: 'Stopped by user',
          lastUpdated: new Date().toISOString()
        }
        
        localStorage.setItem('pipeline-data', JSON.stringify(pipelineData))
        console.log(`✅ Project ${project.project_name} stopped and reset`)
      }
    } catch (error) {
      console.error('❌ Failed to reset project state:', error)
    }
  }

  const handleResetAll = async () => {
    console.log('🔄 Resetting all project states...')
    
    try {
      // Clear API data
      await fetch('/api/pipeline', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      })
      
      // Reset pipeline simulator state
      await pipelineSimulator.resetAllProjects()
      
      // Reset completion report state
      setCompletionReportProject(null)
      setIsCompletionModalOpen(false)
      
      // Force reload projects to refresh stats
      const data = await getJson('/api/projects')
      setProjects(data)
      calculateStats(data)
      
      console.log('✅ All project states reset successfully!')
    } catch (error) {
      console.error('❌ Failed to reset project states:', error)
      // Fallback: force page reload
      window.location.reload()
    }
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

        {/* Project Controls Info */}
        <div className="mb-8 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-700">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Bot className="h-5 w-5 text-blue-600" />
              <h3 className="font-semibold text-blue-900 dark:text-blue-100">Individual Project Controls</h3>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-2 animate-pulse">🧠</div>
              <p className="text-sm font-semibold text-blue-900 dark:text-blue-100">
                Created by Derril Filemon
              </p>
            </div>
          </div>
          <p className="text-sm text-blue-700 dark:text-blue-300 mt-2">
            Use the "Launch" button on each project card to start individual simulations. Projects with active agents will show blinking animations.
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="transition-all duration-300 hover:shadow-xl hover:-translate-y-1" style={{ backgroundColor: '#00FFDE' }}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-800">Total Projects</CardTitle>
              <Target className="h-4 w-4 text-gray-700" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-800">{stats.total}</div>
              <p className="text-xs text-gray-700">
                All AI applications
              </p>
            </CardContent>
          </Card>

          <Card className="transition-all duration-300 hover:shadow-xl hover:-translate-y-1" style={{ backgroundColor: '#5409DA' }}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-white">Completed</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-300" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-300">{stats.complete}</div>
              <p className="text-xs text-gray-200">
                Ready to deploy
              </p>
            </CardContent>
          </Card>

          <Card className="transition-all duration-300 hover:shadow-xl hover:-translate-y-1" style={{ backgroundColor: '#4E71FF' }}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-white">In Progress</CardTitle>
              <Clock className="h-4 w-4 text-yellow-300" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-300">{stats.in_progress}</div>
              <p className="text-xs text-gray-200">
                Currently building
              </p>
            </CardContent>
          </Card>

          <Card className="transition-all duration-300 hover:shadow-xl hover:-translate-y-1" style={{ backgroundColor: '#00CAFF' }}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-800">Not Started</CardTitle>
              <Play className="h-4 w-4 text-gray-700" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-800">{stats.not_started}</div>
              <p className="text-xs text-gray-700">
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
              <div className="flex justify-between items-center">
                <div className="flex items-center gap-4">
                  <span className="text-sm">Progress</span>
                  <span className="text-sm font-medium">{overallProgress}%</span>
                </div>
                <Button
                  onClick={handleResetAll}
                  variant="outline"
                  size="sm"
                  className="text-xs px-3 py-1 h-7 bg-red-50 hover:bg-red-100 text-red-700 border-red-200 hover:border-red-300"
                >
                  <RefreshCw className="h-3 w-3 mr-1" />
                  Reset All
                </Button>
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
              className={`cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-1 hover:scale-[1.02] ${hasActiveAgents ? 'animate-pulse border-red-300 shadow-lg shadow-red-200 bg-red-50' : 'hover:border-blue-200'}`}
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
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    {getStatusBadge(project)}
                    <span className="text-xs text-muted-foreground">
                      {project.progress || 0}% complete
                    </span>
                  </div>
                  
                  {/* Individual Run/Stop Buttons */}
                  <div className="relative flex gap-2">
                    <button
                      disabled={Boolean(project.progress && project.progress > 0)}
                      onClick={(e) => {
                        e.stopPropagation() // Prevent card click
                        handleRunSingleProject(project)
                      }}
                      className={`
                        px-4 py-2 rounded-lg font-medium text-sm border
                        ${project.progress && project.progress > 0 
                          ? 'bg-blue-500 text-white cursor-not-allowed opacity-75 border-blue-600' 
                          : 'bg-green-500 text-white hover:bg-green-600 border-green-600'
                        }
                        disabled:opacity-50 disabled:cursor-not-allowed
                      `}
                    >
                      <div className="flex items-center gap-2">
                        {project.progress && project.progress > 0 && project.progress < 100 ? (
                          <>
                            <div className="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                            <span>Running</span>
                          </>
                        ) : project.progress === 100 ? (
                          <>
                            <CheckCircle className="h-3 w-3" />
                            <span>Complete</span>
                          </>
                        ) : (
                          <>
                            <Play className="h-3 w-3" />
                            <span>Launch</span>
                          </>
                        )}
                      </div>
                    </button>
                    
                    {/* Stop Button */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation() // Prevent card click
                        handleStopProject(project)
                      }}
                      className="w-12 h-10 rounded-lg bg-red-500 hover:bg-red-600 text-white border border-red-600"
                      title="Stop Pipeline"
                    >
                      <div className="flex items-center justify-center h-full">
                        <span className="text-white font-bold">⏹</span>
                      </div>
                    </button>
                    
                    {/* Progress indicator for running state */}
                    {project.progress && project.progress > 0 && project.progress < 100 && (
                      <div className="absolute -bottom-1 left-0 right-0 h-1 bg-gray-200 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all duration-500 ease-out"
                          style={{ width: `${project.progress}%` }}
                        ></div>
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <Code className="h-3 w-3" />
                    <span className="line-clamp-1">{project.tech_stack}</span>
                  </div>
                </div>

                <Progress 
                  value={project.progress || 0} 
                  className={`h-2 ${project.status === 'failed' ? 'bg-red-100' : ''}`}
                  style={project.status === 'failed' ? {
                    backgroundColor: '#fef2f2',
                    '--progress-background': '#ef4444'
                  } as React.CSSProperties : {}}
                />
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

        {/* Final Report Modal */}
        {completionReportProject && (
          <FinalReportModal
            projectName={completionReportProject.project_name}
            isOpen={isCompletionModalOpen}
            onClose={() => {
              setIsCompletionModalOpen(false)
              setCompletionReportProject(null)
            }}
            projectId={completionReportProject.project_name.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9\s-]+/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '')}
          />
        )}
      </div>
    </div>
  )
}
