'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { 
  X, 
  Plus, 
  Trash2, 
  CheckCircle, 
  Circle,
  Calendar,
  Clock,
  Info
} from 'lucide-react'
import { todoManager, type TodoItem, type ProjectTodo } from '@/lib/todo-manager'
import { ProjectDescriptionModal } from './project-description-modal'

interface TodoModalProps {
  project: {
    project_name: string
    description: string
    tech_stack: string
  }
  isOpen: boolean
  onClose: () => void
  onProgressUpdate: (progress: number) => void
}

export function TodoModal({ project, isOpen, onClose, onProgressUpdate }: TodoModalProps) {
  const [projectTodo, setProjectTodo] = useState<ProjectTodo | null>(null)
  const [newTodoText, setNewTodoText] = useState('')
  const [isAdding, setIsAdding] = useState(false)
  const [isDescriptionModalOpen, setIsDescriptionModalOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const projectId = project.project_name.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9\s]+/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '')

  useEffect(() => {
    if (isOpen && project && project.project_name) {
      const loadTodos = async () => {
        setIsLoading(true)
        try {
          // Load from pipeline-todos.json instead of todo manager
          const response = await fetch('/api/pipeline')
          const pipelineData = await response.json()
          const projectData = pipelineData[projectId]
          
          if (projectData) {
            setProjectTodo(projectData)
            updateProgress(projectData)
          } else {
            // Create default pipeline structure
            const defaultTodo: ProjectTodo = {
              projectId,
              projectName: project.project_name || projectId,
              items: [
                { id: 'market-research', text: '🔍 Market Research & Analysis', agent: 'MarketResearcher', completed: false, status: 'pending', timestamp: null },
                { id: 'project-brief', text: '📋 Create Project Brief', agent: 'PromptEngineer', completed: false, status: 'pending', timestamp: null },
                { id: 'prompt-template', text: '🎯 Select & Customize Prompt Template', agent: 'PromptEngineer', completed: false, status: 'pending', timestamp: null },
                { id: 'backend-code', text: '⚙️ Generate Backend Code', agent: 'BackendEngineer', completed: false, status: 'pending', timestamp: null },
                { id: 'frontend-code', text: '🎨 Generate Frontend Code', agent: 'FrontendEngineer', completed: false, status: 'pending', timestamp: null },
                { id: 'integration', text: '🔗 Integration & API Connections', agent: 'BackendEngineer', completed: false, status: 'pending', timestamp: null },
                { id: 'deployment', text: '🚀 Deployment Configuration', agent: 'DeliveryCoordinator', completed: false, status: 'pending', timestamp: null },
                { id: 'validation', text: '✅ Validation & Testing', agent: 'DeliveryCoordinator', completed: false, status: 'pending', timestamp: null }
              ],
              progress: 0,
              activeAgents: [],
              lastUpdated: new Date().toISOString()
            }
            setProjectTodo(defaultTodo)
            updateProgress(defaultTodo)
          }
        } catch (error) {
          console.error('Error loading project todos:', error)
          // Create a fallback todo if there's an error
          const fallbackTodo: ProjectTodo = {
            projectId,
            projectName: project.project_name || projectId,
            items: [],
            progress: 0,
            activeAgents: [],
            lastUpdated: new Date().toISOString()
          }
          setProjectTodo(fallbackTodo)
        } finally {
          setIsLoading(false)
        }
      }
      
      loadTodos()
      
      // Set up real-time updates
      const interval = setInterval(async () => {
        try {
          const response = await fetch('/api/pipeline')
          const pipelineData = await response.json()
          const projectData = pipelineData[projectId]
          
          if (projectData) {
            setProjectTodo(projectData)
            updateProgress(projectData)
          }
        } catch (error) {
          console.error('Error updating project todos:', error)
        }
      }, 2000) // Update every 2 seconds
      
      return () => clearInterval(interval)
    }
  }, [isOpen, project, projectId])

  const updateProgress = (todo: ProjectTodo) => {
    const progress = todo.progress || 0
    onProgressUpdate(progress)
  }

  // Read-only mode - todos are managed by the pipeline simulator
  const handleToggleTodo = async (todoId: string) => {
    // Disabled - todos are managed by the pipeline
    console.log('Todo management is handled by the pipeline simulator')
  }

  const handleAddTodo = async () => {
    // Disabled - todos are managed by the pipeline
    console.log('Todo management is handled by the pipeline simulator')
  }

  const handleDeleteTodo = async (todoId: string) => {
    // Disabled - todos are managed by the pipeline
    console.log('Todo management is handled by the pipeline simulator')
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !isAdding) {
      handleAddTodo()
    }
  }

  if (!isOpen || !projectTodo || isLoading) return null

  // Safety check for items array
  const items = projectTodo.items || []
  const completedCount = items.filter(todo => todo.completed).length
  const totalCount = items.length
  const progress = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="relative w-full max-w-2xl mx-4">
        <Card className="shadow-2xl border-0 bg-white dark:bg-slate-800/95 backdrop-blur-sm">
          <CardHeader className="pb-4">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <CardTitle className="text-xl font-semibold text-gray-900 dark:text-slate-100">
                  {project.project_name || 'Unknown Project'}
                </CardTitle>
                <CardDescription className="text-sm text-gray-600 dark:text-slate-300 mt-1">
                  {project.description || 'No description available'}
                </CardDescription>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setIsDescriptionModalOpen(true)}
                  className="project-details-btn text-xs px-3 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 border-blue-200 dark:bg-blue-900/20 dark:hover:bg-blue-900/30 dark:text-blue-300 dark:border-blue-700"
                >
                  <Info className="h-3 w-3 mr-1" />
                  Project Details
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onClose}
                  className="h-8 w-8 p-0 hover:bg-gray-100 dark:hover:bg-slate-700/50"
                >
                  <X className="h-4 w-4 text-white" />
                </Button>
              </div>
            </div>
            
                         {/* Progress Section */}
             <div className="mt-4 space-y-2">
               <div className="flex items-center justify-between text-sm">
                 <span className="text-gray-600 dark:text-slate-300">Progress</span>
                 <span className="font-medium text-gray-900 dark:text-slate-100">
                   {completedCount} of {totalCount} completed
                 </span>
               </div>
               <Progress value={progress} className="h-2" />
               
               {/* Active Agents Indicator */}
               {projectTodo.activeAgents && projectTodo.activeAgents.length > 0 && (
                 <div className="flex items-center gap-2 text-xs text-blue-600 dark:text-blue-400 animate-pulse">
                   <span>🤖 Active Agents:</span>
                   {projectTodo.activeAgents.map((agent, index) => (
                     <Badge 
                       key={agent} 
                       variant="outline" 
                       className="bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-700"
                     >
                       {agent}
                     </Badge>
                   ))}
                 </div>
               )}
               
               <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-slate-400">
                 <Clock className="h-3 w-3" />
                 <span>Last updated: {new Date(projectTodo.lastUpdated).toLocaleString()}</span>
               </div>
             </div>
          </CardHeader>

          <CardContent className="space-y-4">
            {/* Pipeline Status Info */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 dark:bg-blue-900/20 dark:border-blue-700">
              <div className="flex items-center gap-2 text-sm text-blue-700 dark:text-blue-300">
                <Info className="h-4 w-4" />
                <span className="font-medium">Pipeline Tasks</span>
              </div>
              <p className="text-xs text-blue-600 dark:text-blue-400 mt-1">
                These tasks are automatically managed by the AI pipeline. Progress updates in real-time as agents complete their work.
              </p>
            </div>

            {/* Todo List */}
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {!items || items.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <Circle className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>No tasks yet. Add your first task above!</p>
                </div>
              ) : (
                                 items.map((todo) => (
                   <div
                     key={todo.id}
                     className={`flex items-center gap-3 p-3 rounded-lg border transition-all ${
                       todo.completed
                         ? 'bg-green-50 border-green-200 dark:bg-green-900/10 dark:border-green-700/30'
                         : 'bg-gray-50 border-gray-200 dark:bg-slate-700/30 dark:border-slate-600/50'
                     }`}
                   >
                    <div className="flex-shrink-0">
                      {todo.completed ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : todo.status === 'in_progress' ? (
                        <div className="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                      ) : (
                        <Circle className="h-5 w-5 text-gray-400" />
                      )}
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <p
                        className={`text-sm transition-all ${
                          todo.completed
                            ? 'line-through text-gray-500 dark:text-slate-400'
                            : 'text-gray-900 dark:text-slate-100'
                        }`}
                      >
                        {todo.text}
                      </p>
                      <div className="flex items-center gap-2 mt-1">
                        {todo.agent && (
                          <Badge 
                            variant="outline" 
                            className={`text-xs px-2 py-0.5 ${
                              todo.status === 'in_progress' 
                                ? 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-700 animate-pulse'
                                : 'bg-gray-50 text-gray-600 border-gray-200 dark:bg-slate-700/30 dark:text-slate-400 dark:border-slate-600'
                            }`}
                          >
                            {todo.agent}
                          </Badge>
                        )}
                        {todo.status === 'in_progress' && (
                          <span className="text-xs text-blue-600 dark:text-blue-400 animate-pulse">
                            🔄 Working...
                          </span>
                        )}
                        {todo.status === 'completed' && (
                          <span className="text-xs text-green-600 dark:text-green-400">
                            ✅ Complete
                          </span>
                        )}
                        {todo.status === 'error' && (
                          <span className="text-xs text-red-600 dark:text-red-400">
                            ❌ Error
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>

                         {/* Tech Stack Badge */}
             <div className="pt-4 border-t border-gray-200 dark:border-slate-600/50">
               <div className="flex items-center gap-2">
                 <span className="text-xs text-gray-500 dark:text-slate-400">Tech Stack:</span>
                 <Badge variant="outline" className="text-sm px-3 py-1 text-white bg-slate-600/50 border-slate-500/50">
                   {project.tech_stack}
                 </Badge>
               </div>
             </div>
          </CardContent>
        </Card>
      </div>
      
      {/* Project Description Modal */}
      <ProjectDescriptionModal
        project={project}
        isOpen={isDescriptionModalOpen}
        onClose={() => setIsDescriptionModalOpen(false)}
      />
    </div>
  )
}
