import { NextRequest, NextResponse } from 'next/server'
import { pipelineSimulator } from '@/lib/pipeline-simulator'

export async function POST(request: NextRequest) {
  try {
    console.log('🛑 Stopping pipeline simulation...')
    
    // Stop the pipeline simulator
    await pipelineSimulator.stopSimulation()

    return NextResponse.json({ 
      success: true, 
      message: 'Pipeline simulation stopped' 
    })
  } catch (error) {
    console.error('❌ Stop pipeline failed:', error)
    return NextResponse.json({ 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    }, { status: 500 })
  }
}
