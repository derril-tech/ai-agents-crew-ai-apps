// lib/agent-simulator.ts
import { todoManager } from './todo-manager'

export class AgentSimulator {
  private intervalId: NodeJS.Timeout | null = null
  private isRunning = false

  // Start simulating agents working on projects
  startSimulation() {
    if (this.isRunning) return
    
    this.isRunning = true
    console.log('🤖 Starting Agent Simulation...')
    
    // Simulate agents working on different projects
    this.intervalId = setInterval(() => {
      this.simulateAgentWork()
    }, 3000) // Update every 3 seconds
  }

  // Stop the simulation
  stopSimulation() {
    if (this.intervalId) {
      clearInterval(this.intervalId)
      this.intervalId = null
    }
    this.isRunning = false
    console.log('🛑 Agent Simulation Stopped')
  }

  // Simulate random agent work
  private simulateAgentWork() {
    const projectIds = [
      'ai-powered-code-review-refactoring-assistant',
      'intelligent-document-processing-knowledge-base',
      'ai-powered-resume-parser-job-matcher',
      'real-time-ai-content-moderation-system'
    ]

    const agents = ['MarketResearcher', 'PromptEngineer', 'ClaudeCoder', 'PreCodeValidator']
    const milestones = ['market-research', 'project-brief', 'prompt-template', 'backend-code', 'frontend-code', 'integration', 'deployment', 'validation']

    // Randomly select a project and agent
    const randomProjectId = projectIds[Math.floor(Math.random() * projectIds.length)]
    const randomAgent = agents[Math.floor(Math.random() * agents.length)]
    const randomMilestone = milestones[Math.floor(Math.random() * milestones.length)]

    // Get current project todo
    const projectTodo = todoManager.getProjectTodos(randomProjectId)
    if (!projectTodo) return

    // Find the milestone item
    const milestoneItem = projectTodo.items.find(item => item.id === randomMilestone)
    if (!milestoneItem) return

    // Simulate different actions based on current status
    if (milestoneItem.status === 'pending') {
      // Start working on this milestone
      todoManager.startAgentWork(randomProjectId, randomAgent, randomMilestone)
      console.log(`🤖 ${randomAgent} started working on ${randomMilestone} for ${randomProjectId}`)
    } else if (milestoneItem.status === 'in_progress' && Math.random() > 0.7) {
      // 30% chance to complete the work
      todoManager.completeAgentWork(randomProjectId, randomMilestone)
      console.log(`✅ ${randomAgent} completed ${randomMilestone} for ${randomProjectId}`)
    }
  }

  // Manually trigger agent work for testing
  triggerAgentWork(projectId: string, agent: string, milestoneId: string) {
    todoManager.startAgentWork(projectId, agent, milestoneId)
    console.log(`🤖 Manual trigger: ${agent} started working on ${milestoneId} for ${projectId}`)
  }

  // Manually complete agent work for testing
  completeAgentWork(projectId: string, milestoneId: string) {
    todoManager.completeAgentWork(projectId, milestoneId)
    console.log(`✅ Manual completion: ${milestoneId} for ${projectId}`)
  }

  // Reset all project todos
  resetAllProjects() {
    // Clear all todos and start fresh
    todoManager.clearAllTodos()
    console.log('🔄 All projects reset to initial state')
  }
}

export const agentSimulator = new AgentSimulator()
