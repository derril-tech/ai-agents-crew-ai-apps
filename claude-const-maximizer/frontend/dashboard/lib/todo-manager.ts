// lib/todo-manager.ts
export interface TodoItem {
  id: string
  text: string
  completed: boolean
  agent?: string // Which agent is working on this
  status?: 'pending' | 'in_progress' | 'completed' | 'error'
  timestamp?: string
}

export interface ProjectTodo {
  projectId: string
  projectName: string
  items: TodoItem[]
  progress: number
  activeAgents: string[] // Which agents are currently working
  lastUpdated: string
  status?: string // Overall project status
}

class TodoManager {
  private storageKey = 'project-todos'
  private pipelineKey = 'pipeline-todos' // New key for pipeline integration

  // Pipeline milestones that match our Phase 3 workflow
  private getPipelineMilestones(): TodoItem[] {
    return [
      {
        id: 'market-research',
        text: '🔍 Market Research & Analysis',
        completed: false,
        agent: 'MarketResearcher',
        status: 'pending'
      },
      {
        id: 'project-brief',
        text: '📋 Create Project Brief',
        completed: false,
        agent: 'PromptEngineer',
        status: 'pending'
      },
      {
        id: 'prompt-template',
        text: '🎯 Select & Customize Prompt Template',
        completed: false,
        agent: 'PromptEngineer',
        status: 'pending'
      },
      {
        id: 'backend-code',
        text: '⚙️ Generate Backend Code',
        completed: false,
        agent: 'ClaudeCoder',
        status: 'pending'
      },
      {
        id: 'frontend-code',
        text: '🎨 Generate Frontend Code',
        completed: false,
        agent: 'ClaudeCoder',
        status: 'pending'
      },
      {
        id: 'integration',
        text: '🔗 Integration & API Connections',
        completed: false,
        agent: 'ClaudeCoder',
        status: 'pending'
      },
      {
        id: 'deployment',
        text: '🚀 Deployment Configuration',
        completed: false,
        agent: 'ClaudeCoder',
        status: 'pending'
      },
      {
        id: 'validation',
        text: '✅ Validation & Testing',
        completed: false,
        agent: 'PreCodeValidator',
        status: 'pending'
      }
    ]
  }

  // Get pipeline todos from the integration file
  private async getPipelineTodos(): Promise<ProjectTodo[]> {
    try {
      // Fetch from API endpoint
      const response = await fetch('/api/pipeline')
      if (response.ok) {
        const data = await response.json()
        if (typeof data === 'object' && data !== null) {
          return Object.values(data)
        }
      }
    } catch (error) {
      console.error('Error loading pipeline todos:', error)
    }
    
    return []
  }

  // Get all todos from storage (combines local and pipeline data)
  async getAllTodos(): Promise<ProjectTodo[]> {
    if (typeof window === 'undefined') return []
    
    const localTodos = this.getLocalTodos()
    const pipelineTodos = await this.getPipelineTodos()
    
    // Merge pipeline data with local data (pipeline takes precedence)
    const mergedTodos = new Map<string, ProjectTodo>()
    
    // Add local todos first
    localTodos.forEach(todo => {
      mergedTodos.set(todo.projectId, todo)
    })
    
    // Override with pipeline data
    pipelineTodos.forEach(todo => {
      mergedTodos.set(todo.projectId, todo)
    })
    
    return Array.from(mergedTodos.values())
  }

  // Get local todos from localStorage
  private getLocalTodos(): ProjectTodo[] {
    try {
      const stored = localStorage.getItem(this.storageKey)
      if (!stored) return []
      
      const parsed = JSON.parse(stored)
      
      // Handle both old format (object) and new format (array)
      if (Array.isArray(parsed)) {
        return parsed
      } else if (typeof parsed === 'object' && parsed !== null) {
        // Convert old format to new format
        return Object.values(parsed)
      }
    } catch (error) {
      console.error('Error loading local todos:', error)
    }
    
    return []
  }

  // Save all todos to storage
  private saveTodos(todos: ProjectTodo[]): void {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(todos))
    } catch (error) {
      console.error('Error saving todos:', error)
    }
  }

  // Get todos for a specific project
  getTodos(projectId: string): ProjectTodo {
    this.getAllTodos().then(todos => {
      const existing = todos.find((t: ProjectTodo) => t.projectId === projectId)
      
      if (existing) {
        // Ensure items array exists (fix for old data)
        if (!existing.items) {
          existing.items = this.getPipelineMilestones()
          existing.progress = 0
          existing.activeAgents = []
          existing.lastUpdated = new Date().toISOString()
          this.saveTodos(todos)
        }
        return existing
      }

      // Create new todo list with pipeline milestones
      const newTodo: ProjectTodo = {
        projectId,
        projectName: projectId, // Will be updated when we have the actual name
        items: this.getPipelineMilestones(),
        progress: 0,
        activeAgents: [],
        lastUpdated: new Date().toISOString()
      }

      todos.push(newTodo)
      this.saveTodos(todos)
      return newTodo
    }).catch(error => {
      console.error('Error fetching todos for project:', error)
      throw new Error('Failed to get project todos')
    })
  }

  // Get todos for a specific project (alias for compatibility)
  getProjectTodos(projectId: string): ProjectTodo | null {
    this.getAllTodos().then(allTodos => {
      const projectTodo = allTodos.find((t: ProjectTodo) => t.projectId === projectId)
      
      if (projectTodo) {
        // Ensure items array exists (fix for old data)
        if (!projectTodo.items) {
          projectTodo.items = this.getPipelineMilestones()
          projectTodo.progress = 0
          projectTodo.activeAgents = []
          projectTodo.lastUpdated = new Date().toISOString()
          this.saveTodos(allTodos)
        }
      }
      
      return projectTodo || null
    }).catch(error => {
      console.error('Error fetching project todos:', error)
      return null
    })
  }

  // Add a new todo item
  addTodo(projectId: string, text: string): TodoItem {
    this.getProjectTodos(projectId).then(projectTodo => {
      if (!projectTodo) throw new Error('Project not found')
      
      const newTodo: TodoItem = {
        id: this.generateId(),
        text,
        completed: false,
        status: 'pending'
      }
      
      projectTodo.items.push(newTodo)
      projectTodo.lastUpdated = new Date().toISOString()
      this.saveProjectTodos(projectId, projectTodo)
      
      return newTodo
    }).catch(error => {
      console.error('Error adding todo:', error)
      throw new Error('Failed to add todo')
    })
  }
  
  // Toggle todo completion
  toggleTodo(projectId: string, todoId: string): TodoItem | null {
    this.getProjectTodos(projectId).then(projectTodo => {
      if (!projectTodo) return null
      
      const todo = projectTodo.items.find((t: TodoItem) => t.id === todoId)
      if (!todo) return null
      
      todo.completed = !todo.completed
      todo.status = todo.completed ? 'completed' : 'pending'
      
      projectTodo.lastUpdated = new Date().toISOString()
      this.saveProjectTodos(projectId, projectTodo)
      
      return todo
    }).catch(error => {
      console.error('Error toggling todo:', error)
      return null
    })
  }
  
  // Delete a todo item
  deleteTodo(projectId: string, todoId: string): boolean {
    this.getProjectTodos(projectId).then(projectTodo => {
      if (!projectTodo) return false
      
      const initialLength = projectTodo.items.length
      projectTodo.items = projectTodo.items.filter((t: TodoItem) => t.id !== todoId)
      
      if (projectTodo.items.length !== initialLength) {
        projectTodo.lastUpdated = new Date().toISOString()
        this.saveProjectTodos(projectId, projectTodo)
        return true
      }
      
      return false
    }).catch(error => {
      console.error('Error deleting todo:', error)
      return false
    })
  }

  // Calculate progress percentage
  private calculateProgress(items: TodoItem[]): number {
    if (items.length === 0) return 0
    const completedCount = items.filter(item => item.completed).length
    return Math.round((completedCount / items.length) * 100)
  }

  // Get progress percentage for a project
  getProgressPercentage(projectId: string): number {
    this.getProjectTodos(projectId).then(projectTodo => {
      if (!projectTodo || projectTodo.items.length === 0) return 0
      
      return this.calculateProgress(projectTodo.items)
    }).catch(error => {
      console.error('Error getting progress percentage:', error)
      return 0
    })
  }

  // Update item status (for agent integration)
  updateItemStatus(projectId: string, itemId: string, status: TodoItem['status'], agent?: string): void {
    this.getAllTodos().then(todos => {
      const projectTodo = todos.find((t: ProjectTodo) => t.projectId === projectId)
      
      if (projectTodo) {
        const item = projectTodo.items.find((i: TodoItem) => i.id === itemId)
        if (item) {
          item.status = status
          item.completed = status === 'completed'
          if (agent) item.agent = agent
          if (status === 'in_progress') {
            item.timestamp = new Date().toISOString()
          }
          
          // Update active agents
          this.updateActiveAgents(projectTodo)
          
          // Recalculate progress
          projectTodo.progress = this.calculateProgress(projectTodo.items)
          projectTodo.lastUpdated = new Date().toISOString()
          
          this.saveTodos(todos)
        }
      }
    }).catch(error => {
      console.error('Error updating item status:', error)
    })
  }

  private updateActiveAgents(projectTodo: ProjectTodo): void {
    const activeAgents = projectTodo.items
      .filter(item => item.status === 'in_progress')
      .map(item => item.agent)
      .filter(Boolean) as string[]
    
    projectTodo.activeAgents = Array.from(new Set(activeAgents)) // Remove duplicates
  }

  // Method to simulate agent starting work (for testing)
  startAgentWork(projectId: string, agent: string, itemId: string): void {
    this.updateItemStatus(projectId, itemId, 'in_progress', agent)
  }

  // Method to simulate agent completing work (for testing)
  completeAgentWork(projectId: string, itemId: string): void {
    this.updateItemStatus(projectId, itemId, 'completed')
  }

  // Clear all todos (useful for resetting)
  clearAllTodos(): void {
    try {
      localStorage.removeItem(this.storageKey)
      console.log('🧹 All todos cleared from localStorage')
    } catch (error) {
      console.error('Error clearing todos:', error)
    }
  }

  // Save project todos to localStorage
  private saveProjectTodos(projectId: string, projectTodo: ProjectTodo): void {
    try {
      this.getAllTodos().then(allTodos => {
        const index = allTodos.findIndex((t: ProjectTodo) => t.projectId === projectId)
        if (index !== -1) {
          allTodos[index] = projectTodo
        } else {
          allTodos.push(projectTodo)
        }
        localStorage.setItem(this.storageKey, JSON.stringify(allTodos))
      }).catch(error => {
        console.error('Error saving todos:', error)
      })
    } catch (error) {
      console.error('Error saving todos:', error)
    }
  }
  
  // Generate unique ID
  private generateId(): string {
    return Math.random().toString(36).substr(2, 9) + Date.now().toString(36)
  }
}

export const todoManager = new TodoManager()
