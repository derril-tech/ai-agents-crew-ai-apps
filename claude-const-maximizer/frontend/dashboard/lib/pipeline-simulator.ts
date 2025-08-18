// Note: This simulator runs in the browser, so we use localStorage instead of fs
// For server-side operations, we'll use API calls

interface PipelineItem {
  id: string
  text: string
  completed: boolean
  agent: string
  status: 'completed' | 'in_progress' | 'pending'
  timestamp: string | null
}

interface PipelineProject {
  projectId: string
  projectName: string
  items: PipelineItem[]
  progress: number
  activeAgents: string[]
  lastUpdated: string
}

const AGENTS = [
  'MarketResearcher',
  'PromptEngineer', 
  'FrontendEngineer',
  'BackendEngineer',
  'DeliveryCoordinator'
]

const TASKS = [
  { id: 'market-research', text: '🔍 Market Research & Analysis', agent: 'MarketResearcher' },
  { id: 'project-brief', text: '📋 Create Project Brief', agent: 'PromptEngineer' },
  { id: 'prompt-template', text: '🎯 Select & Customize Prompt Template', agent: 'PromptEngineer' },
  { id: 'backend-code', text: '⚙️ Generate Backend Code', agent: 'BackendEngineer' },
  { id: 'frontend-code', text: '🎨 Generate Frontend Code', agent: 'FrontendEngineer' },
  { id: 'integration', text: '🔗 Integration & API Connections', agent: 'BackendEngineer' },
  { id: 'deployment', text: '🚀 Deployment Configuration', agent: 'DeliveryCoordinator' },
  { id: 'validation', text: '✅ Validation & Testing', agent: 'DeliveryCoordinator' }
]

export class PipelineSimulator {
  private interval: NodeJS.Timeout | null = null
  private currentStep = 0

  constructor() {
    // Initialize with test data
    this.initializeTestData()
  }

  private initializeTestData() {
    if (typeof window !== 'undefined') {
      const existing = localStorage.getItem('pipeline-data')
      if (!existing) {
        // Add test data for the first project
        const testData = {
          'ai-powered-code-review-and-refactoring-assistant': {
            projectId: 'ai-powered-code-review-and-refactoring-assistant',
            projectName: 'AI-Powered Code Review & Refactoring Assistant',
            items: TASKS.map(task => ({
              ...task,
              completed: false,
              status: 'pending' as const,
              timestamp: null
            })),
            progress: 25,
            activeAgents: ['PromptEngineer'],
            lastUpdated: new Date().toISOString()
          }
        }
        localStorage.setItem('pipeline-data', JSON.stringify(testData))
        console.log('✅ Test data initialized')
      }
    }
  }

  async startSimulation() {
    // Default to the first project for backward compatibility
    await this.startSimulationForProject('ai-powered-code-review-and-refactoring-assistant', 'AI-Powered Code Review & Refactoring Assistant')
  }

  async startSimulationForProject(projectId: string, projectName: string) {
    console.log(`🚀 Starting pipeline simulation for: ${projectName}`)
    
    // Stop any existing simulation first
    if (this.interval) {
      clearInterval(this.interval)
      this.interval = null
    }
    
    // Reset current step
    this.currentStep = 0
    
    // Initialize pipeline data for the specific project
    const initialData = {
      [projectId]: {
        projectId,
        projectName,
        items: TASKS.map(task => ({
          ...task,
          completed: false,
          status: 'pending' as const,
          timestamp: null
        })),
        progress: 0,
        activeAgents: [AGENTS[0]],
        lastUpdated: new Date().toISOString()
      }
    }
    
    console.log('📊 Initial data:', initialData)
    await this.savePipelineData(initialData)
    console.log('✅ Initial data saved')
    
    // Start simulation loop - faster for testing
    this.interval = setInterval(async () => {
      console.log(`🔄 Simulation step ${this.currentStep + 1} for ${projectName}`)
      await this.simulateNextStep(projectId)
    }, 3000) // Update every 3 seconds for testing
    
    console.log('✅ Simulation interval started')
  }

  async stopSimulation() {
    if (this.interval) {
      clearInterval(this.interval)
      this.interval = null
    }
    
    console.log('🛑 Pipeline simulation stopped')
    
    // Clear active agents
    const data = await this.loadPipelineData()
    Object.keys(data).forEach(projectId => {
      if (data[projectId]) {
        data[projectId].activeAgents = []
        data[projectId].lastUpdated = new Date().toISOString()
      }
    })
    
    await this.savePipelineData(data)
  }

  private async simulateNextStep(projectId: string) {
    try {
      console.log(`🔄 Starting step ${this.currentStep + 1} for project ${projectId}`)
      
      const data = await this.loadPipelineData()
      console.log('📊 Loaded data:', data)
      
      const project = data[projectId]
      console.log('📋 Project data:', project)
      
      if (!project) {
        console.log('❌ No project data found, stopping simulation')
        if (this.interval) {
          clearInterval(this.interval)
          this.interval = null
        }
        return
      }
      
      if (this.currentStep >= TASKS.length) {
        console.log('🎉 Pipeline simulation completed!')
        if (this.interval) {
          clearInterval(this.interval)
          this.interval = null
        }
        return
      }
      
      // Update current task
      const task = TASKS[this.currentStep]
      console.log(`📝 Updating task: ${task.text}`)
      
      const taskIndex = project.items.findIndex(item => item.id === task.id)
      
      if (taskIndex !== -1) {
        project.items[taskIndex].completed = true
        project.items[taskIndex].status = 'completed'
        project.items[taskIndex].timestamp = new Date().toISOString()
      }
      
      // Move to next task
      this.currentStep++
      
      if (this.currentStep < TASKS.length) {
        const nextTask = TASKS[this.currentStep]
        const nextTaskIndex = project.items.findIndex(item => item.id === nextTask.id)
        
        if (nextTaskIndex !== -1) {
          project.items[nextTaskIndex].status = 'in_progress'
          project.activeAgents = [nextTask.agent]
        }
      } else {
        // All tasks completed
        project.activeAgents = []
      }
      
      // Update progress
      project.progress = Math.round((this.currentStep / TASKS.length) * 100)
      project.lastUpdated = new Date().toISOString()
      
      console.log(`💾 Saving data with progress: ${project.progress}%`)
      await this.savePipelineData(data)
      console.log(`✅ Data saved successfully`)
      
      console.log(`📊 Progress: ${project.progress}% - ${task.agent} completed`)
      
      // Only stop simulation after completion is shown for a bit
      if (project.progress === 100) {
        console.log('🎉 All tasks completed, will stop in 5 seconds')
        setTimeout(() => {
          if (this.interval) {
            clearInterval(this.interval)
            this.interval = null
            console.log('🛑 Simulation stopped after completion')
          }
        }, 5000)
      }
    } catch (error) {
      console.error('❌ Error in simulateNextStep:', error)
      // Don't stop simulation on error, just log it
    }
  }

  private async loadPipelineData(): Promise<Record<string, PipelineProject>> {
    try {
      if (typeof window !== 'undefined') {
        // Use localStorage for immediate testing
        const stored = localStorage.getItem('pipeline-data')
        if (stored) {
          return JSON.parse(stored)
        }
      }
      return {}
    } catch {
      return {}
    }
  }

  private async savePipelineData(data: Record<string, PipelineProject>) {
    if (typeof window !== 'undefined') {
      try {
        // Use localStorage for immediate testing
        localStorage.setItem('pipeline-data', JSON.stringify(data))
        console.log('✅ Data saved to localStorage:', data)
      } catch (error) {
        console.error('Failed to save pipeline data:', error)
      }
    }
  }

  async resetSimulation() {
    this.currentStep = 0
    await this.savePipelineData({})
    console.log('🔄 Pipeline simulation reset')
  }

  async resetAllProjects() {
    // Clear all project data and reset to initial state
    await this.savePipelineData({})
    console.log('🔄 All projects reset to initial state')
  }
}

// Export singleton instance
export const pipelineSimulator = new PipelineSimulator()
