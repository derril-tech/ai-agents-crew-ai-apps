import { NextResponse } from 'next/server'
import { readFileSync } from 'fs'
import { join } from 'path'

export async function GET() {
  try {
    // Read projects from the root directory
    const projectsPath = join(process.cwd(), '..', '..', 'projects.json')
    const projectsData = readFileSync(projectsPath, 'utf-8')
    const projects = JSON.parse(projectsData)
    
    return NextResponse.json(projects)
  } catch (error) {
    console.error('Error loading projects:', error)
    return NextResponse.json({ error: 'Failed to load projects' }, { status: 500 })
  }
}
