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
          const todo = await todoManager.getTodos(projectId)
          setProjectTodo(todo)
          updateProgress(todo)
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
    }
  }, [isOpen, project, projectId])

  const updateProgress = (todo: ProjectTodo) => {
    const progress = todo.progress || 0
    onProgressUpdate(progress)
  }

  const handleToggleTodo = async (todoId: string) => {
    if (!projectTodo) return

    try {
      const updatedTodo = await todoManager.toggleTodo(projectId, todoId)
      if (updatedTodo) {
        const updatedProjectTodo = await todoManager.getProjectTodos(projectId)
        if (updatedProjectTodo) {
          setProjectTodo(updatedProjectTodo)
          updateProgress(updatedProjectTodo)
        }
      }
    } catch (error) {
      console.error('Error toggling todo:', error)
    }
  }

  const handleAddTodo = async () => {
    if (!newTodoText.trim() || !projectTodo) return

    setIsAdding(true)
    try {
      const newTodo = await todoManager.addTodo(projectId, newTodoText.trim())
      const updatedProjectTodo = await todoManager.getProjectTodos(projectId)
      if (updatedProjectTodo) {
        setProjectTodo(updatedProjectTodo)
        updateProgress(updatedProjectTodo)
      }
      setNewTodoText('')
    } catch (error) {
      console.error('Error adding todo:', error)
    } finally {
      setIsAdding(false)
    }
  }

  const handleDeleteTodo = async (todoId: string) => {
    if (!projectTodo) return

    try {
      const success = await todoManager.deleteTodo(projectId, todoId)
      if (success) {
        const updatedProjectTodo = await todoManager.getProjectTodos(projectId)
        if (updatedProjectTodo) {
          setProjectTodo(updatedProjectTodo)
          updateProgress(updatedProjectTodo)
        }
      }
    } catch (error) {
      console.error('Error deleting todo:', error)
    }
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
            {/* Add New Todo */}
            <div className="flex gap-2">
              <Input
                placeholder="Add a new task..."
                value={newTodoText}
                onChange={(e) => setNewTodoText(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isAdding}
                className="flex-1"
              />
              <Button
                onClick={handleAddTodo}
                disabled={!newTodoText.trim() || isAdding}
                size="sm"
                className="px-3"
              >
                <Plus className="h-4 w-4" />
              </Button>
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
                    <button
                      onClick={() => handleToggleTodo(todo.id)}
                      className={`flex-shrink-0 transition-colors ${
                        todo.completed
                          ? 'text-green-600 hover:text-green-700'
                          : 'text-gray-400 hover:text-gray-600'
                      }`}
                    >
                      {todo.completed ? (
                        <CheckCircle className="h-5 w-5" />
                      ) : (
                        <Circle className="h-5 w-5" />
                      )}
                    </button>
                    
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
                    
                                         <Button
                       variant="ghost"
                       size="sm"
                       onClick={() => handleDeleteTodo(todo.id)}
                       className="h-6 w-6 p-0 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:text-slate-400 dark:hover:text-red-400 dark:hover:bg-red-900/10"
                     >
                      <Trash2 className="h-3 w-3" />
                    </Button>
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
