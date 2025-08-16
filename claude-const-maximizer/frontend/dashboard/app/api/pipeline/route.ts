import { NextRequest, NextResponse } from 'next/server'
import { promises as fs } from 'fs'
import path from 'path'

export async function GET(request: NextRequest) {
  try {
    // Path to the pipeline todos file
    const pipelineTodosPath = path.join(process.cwd(), 'lib', 'pipeline-todos.json')
    
    // Check if file exists
    try {
      await fs.access(pipelineTodosPath)
    } catch {
      // File doesn't exist, return empty data
      return NextResponse.json({})
    }
    
    // Read the pipeline todos file
    const pipelineData = await fs.readFile(pipelineTodosPath, 'utf-8')
    const todos = JSON.parse(pipelineData)
    
    return NextResponse.json(todos)
  } catch (error) {
    console.error('Error reading pipeline todos:', error)
    return NextResponse.json({ error: 'Failed to load pipeline data' }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { projectId, todos } = body
    
    // Path to the pipeline todos file
    const pipelineTodosPath = path.join(process.cwd(), 'lib', 'pipeline-todos.json')
    
    // Read existing data
    let existingData = {}
    try {
      const existingContent = await fs.readFile(pipelineTodosPath, 'utf-8')
      existingData = JSON.parse(existingContent)
    } catch {
      // File doesn't exist, start with empty object
    }
    
    // Update with new data
    existingData[projectId] = todos
    
    // Write back to file
    await fs.writeFile(pipelineTodosPath, JSON.stringify(existingData, null, 2))
    
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error updating pipeline todos:', error)
    return NextResponse.json({ error: 'Failed to update pipeline data' }, { status: 500 })
  }
}
