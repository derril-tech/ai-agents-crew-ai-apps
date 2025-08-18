import { NextRequest, NextResponse } from 'next/server'
import { pipelineSimulator } from '@/lib/pipeline-simulator'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { projectId, projectName } = body
    
    console.log(`🚀 Starting REAL CrewAI pipeline for: ${projectName} (${projectId})`)
    
    // Start simulation for UI feedback (immediate response)
    await pipelineSimulator.startSimulationForProject(projectId, projectName)
    
    // Call the real CrewAI pipeline
    try {
      const response = await fetch('http://localhost:8001/api/run-crewai-project', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectName })
      })
      
      if (!response.ok) {
        throw new Error(`CrewAI API error: ${response.status}`)
      }
      
      const crewResult = await response.json()
      console.log('✅ Real CrewAI pipeline result:', crewResult)
    } catch (crewError) {
      console.error('❌ Real CrewAI pipeline failed, continuing with simulation:', crewError)
      // Continue with simulation if real pipeline fails
    }

    return NextResponse.json({
      success: true,
      message: `Pipeline started for ${projectName}`,
      projectId,
      projectName
    })
  } catch (error) {
    console.error('❌ Single project pipeline failed:', error)
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}
