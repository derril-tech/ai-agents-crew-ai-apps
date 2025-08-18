'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  CheckCircle, 
  FileText, 
  Code, 
  Database, 
  Globe, 
  Download,
  X,
  Clock,
  DollarSign,
  Users,
  AlertCircle
} from 'lucide-react'

interface CompletionReport {
  projectId: string
  status: string
  completionDate: string
  deliverables: {
    market_research: string
    project_brief: string
    prompt_template: string
    generated_code: string
    validation_report: string
  }
  summary: {
    totalFiles: number
    agentsUsed: string[]
    estimatedValue: string
    developmentTime: string
  }
}

interface CompletionReportModalProps {
  projectName: string
  isOpen: boolean
  onClose: () => void
  projectId: string
}

export function CompletionReportModal({ 
  projectName, 
  isOpen, 
  onClose, 
  projectId 
}: CompletionReportModalProps) {
  const [report, setReport] = useState<CompletionReport | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (isOpen && projectId) {
      loadCompletionReport()
    }
  }, [isOpen, projectId])

  const loadCompletionReport = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`/api/pipeline-complete/${projectId}`)
      if (!response.ok) {
        throw new Error('Failed to load completion report')
      }
      
      const data = await response.json()
      setReport(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <CheckCircle className="h-8 w-8 text-green-500" />
              <div>
                <h2 className="text-2xl font-bold">Project Complete! 🎉</h2>
                <p className="text-gray-600">{projectName}</p>
              </div>
            </div>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>

          {loading && (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-2 text-gray-600">Loading completion report...</p>
            </div>
          )}

          {error && (
            <div className="text-center py-8">
              <AlertCircle className="h-8 w-8 text-red-500 mx-auto mb-2" />
              <p className="text-red-600">Error: {error}</p>
            </div>
          )}

          {report && (
            <div className="space-y-6">
              {/* Summary Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <Card>
                  <CardContent className="p-4 text-center">
                    <FileText className="h-6 w-6 text-blue-500 mx-auto mb-2" />
                    <div className="text-2xl font-bold">{report.summary.totalFiles}</div>
                    <p className="text-sm text-gray-600">Files Generated</p>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardContent className="p-4 text-center">
                    <Users className="h-6 w-6 text-green-500 mx-auto mb-2" />
                    <div className="text-2xl font-bold">{report.summary.agentsUsed.length}</div>
                    <p className="text-sm text-gray-600">AI Agents Used</p>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardContent className="p-4 text-center">
                    <DollarSign className="h-6 w-6 text-yellow-500 mx-auto mb-2" />
                    <div className="text-lg font-bold">{report.summary.estimatedValue}</div>
                    <p className="text-sm text-gray-600">Estimated Value</p>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardContent className="p-4 text-center">
                    <Clock className="h-6 w-6 text-purple-500 mx-auto mb-2" />
                    <div className="text-lg font-bold">{report.summary.developmentTime}</div>
                    <p className="text-sm text-gray-600">Dev Time Saved</p>
                  </CardContent>
                </Card>
              </div>

              {/* Deliverables */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Code className="h-5 w-5" />
                    Generated Deliverables
                  </CardTitle>
                  <CardDescription>
                    All files and documentation created by the AI pipeline
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-3">
                      <div className="flex items-center gap-2">
                        <FileText className="h-4 w-4 text-blue-500" />
                        <span className="font-medium">Market Research</span>
                        <Badge variant="outline" className="text-green-600">Complete</Badge>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <FileText className="h-4 w-4 text-green-500" />
                        <span className="font-medium">Project Brief</span>
                        <Badge variant="outline" className="text-green-600">Complete</Badge>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <FileText className="h-4 w-4 text-purple-500" />
                        <span className="font-medium">Prompt Template</span>
                        <Badge variant="outline" className="text-green-600">Complete</Badge>
                      </div>
                    </div>
                    
                    <div className="space-y-3">
                      <div className="flex items-center gap-2">
                        <Code className="h-4 w-4 text-orange-500" />
                        <span className="font-medium">Generated Code</span>
                        <Badge variant="outline" className="text-green-600">Complete</Badge>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <Database className="h-4 w-4 text-red-500" />
                        <span className="font-medium">Validation Report</span>
                        <Badge variant="outline" className="text-green-600">Complete</Badge>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <Globe className="h-4 w-4 text-indigo-500" />
                        <span className="font-medium">Deployment Config</span>
                        <Badge variant="outline" className="text-green-600">Complete</Badge>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* AI Agents Used */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Users className="h-5 w-5" />
                    AI Agents That Worked on This Project
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {report.summary.agentsUsed.map((agent, index) => (
                      <Badge key={index} variant="secondary" className="text-sm">
                        {agent}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Action Buttons */}
              <div className="flex gap-4 justify-end">
                <Button variant="outline" onClick={onClose}>
                  Close
                </Button>
                <Button className="flex items-center gap-2">
                  <Download className="h-4 w-4" />
                  Download Report
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
