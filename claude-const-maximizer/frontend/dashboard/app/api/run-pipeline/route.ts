import { NextRequest, NextResponse } from 'next/server'
import { pipelineSimulator } from '@/lib/pipeline-simulator'

export async function POST(request: NextRequest) {
  try {
    console.log('🚀 Starting pipeline simulation...')
    
    // Start the pipeline simulator
    await pipelineSimulator.startSimulation()

    return NextResponse.json({ 
      success: true, 
      message: 'Pipeline simulation started successfully'
    })
  } catch (error) {
    console.error('❌ Pipeline simulation failed:', error)
    return NextResponse.json({ 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    }, { status: 500 })
  }
}
