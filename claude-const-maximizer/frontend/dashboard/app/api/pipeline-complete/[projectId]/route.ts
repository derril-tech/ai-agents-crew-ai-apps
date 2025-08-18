import { NextRequest, NextResponse } from 'next/server'
import { promises as fs } from 'fs'
import path from 'path'

export async function GET(
  request: NextRequest,
  { params }: { params: { projectId: string } }
) {
  try {
    const { projectId } = params
    
    // Check if project deliverables exist
    const deliverablesPath = path.join(process.cwd(), '..', 'deliverables', projectId)
    
    try {
      await fs.access(deliverablesPath)
    } catch {
      return NextResponse.json(
        { error: 'Project deliverables not found' }, 
        { status: 404 }
      )
    }
    
    // Count total files
    const countFiles = async (dir: string): Promise<number> => {
      let count = 0
      const entries = await fs.readdir(dir, { withFileTypes: true })
      
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name)
        if (entry.isDirectory()) {
          count += await countFiles(fullPath)
        } else {
          count++
        }
      }
      return count
    }
    
    const totalFiles = await countFiles(deliverablesPath)
    
    // Generate completion report
    const report = {
      projectId,
      status: 'completed',
      completionDate: new Date().toISOString(),
      deliverables: {
        market_research: path.join(deliverablesPath, 'market_research.json'),
        project_brief: path.join(deliverablesPath, 'project_brief.md'),
        prompt_template: path.join(deliverablesPath, 'prompt_template.json'),
        generated_code: path.join(deliverablesPath, 'generated_code'),
        validation_report: path.join(deliverablesPath, 'validation_report.json')
      },
      summary: {
        totalFiles,
        agentsUsed: [
          'MarketResearcher',
          'PromptEngineer', 
          'FrontendEngineer',
          'BackendEngineer',
          'DeliveryCoordinator'
        ],
        estimatedValue: '$50,000+',
        developmentTime: '2-3 weeks'
      }
    }
    
    return NextResponse.json(report)
  } catch (error) {
    console.error('Error generating completion report:', error)
    return NextResponse.json(
      { error: 'Failed to generate completion report' }, 
      { status: 500 }
    )
  }
}
