'use client'

import { useState, useRef, useEffect } from 'react'
import { Editor } from '@monaco-editor/react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Play, 
  Shield, 
  Zap, 
  AlertTriangle, 
  CheckCircle, 
  Code2,
  Download,
  Upload,
  Settings
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface CodeEditorProps {
  initialValue?: string
  language?: string
  onCodeChange?: (value: string) => void
  onAnalysis?: (analysis: CodeAnalysis) => void
  className?: string
}

interface CodeAnalysis {
  securityIssues: SecurityIssue[]
  performanceIssues: PerformanceIssue[]
  refactoringSuggestions: RefactoringSuggestion[]
  codeQuality: CodeQualityMetrics
}

interface SecurityIssue {
  line: number
  severity: 'high' | 'medium' | 'low'
  message: string
  category: string
  suggestion: string
}

interface PerformanceIssue {
  line: number
  impact: 'high' | 'medium' | 'low'
  message: string
  optimization: string
}

interface RefactoringSuggestion {
  line: number
  type: 'extract' | 'simplify' | 'optimize' | 'modernize'
  message: string
  before: string
  after: string
}

interface CodeQualityMetrics {
  complexity: number
  maintainability: number
  testability: number
  readability: number
}

export function CodeEditor({
  initialValue = '// Start coding here...',
  language = 'typescript',
  onCodeChange,
  onAnalysis,
  className
}: CodeEditorProps) {
  const [code, setCode] = useState(initialValue)
  const [analysis, setAnalysis] = useState<CodeAnalysis | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [activeTab, setActiveTab] = useState('editor')
  const editorRef = useRef<any>(null)

  const handleEditorDidMount = (editor: any) => {
    editorRef.current = editor
    editor.focus()
  }

  const handleCodeChange = (value: string = '') => {
    setCode(value)
    onCodeChange?.(value)
  }

  const analyzeCode = async () => {
    setIsAnalyzing(true)
    try {
      // Simulate AI analysis - replace with actual API call
      const mockAnalysis: CodeAnalysis = {
        securityIssues: [
          {
            line: 15,
            severity: 'high',
            message: 'SQL injection vulnerability detected',
            category: 'security',
            suggestion: 'Use parameterized queries'
          }
        ],
        performanceIssues: [
          {
            line: 23,
            impact: 'medium',
            message: 'Inefficient loop detected',
            optimization: 'Consider using map() instead of forEach()'
          }
        ],
        refactoringSuggestions: [
          {
            line: 8,
            type: 'extract',
            message: 'Extract function for better readability',
            before: 'const result = data.filter(item => item.active).map(item => item.name)',
            after: 'const getActiveNames = (data) => data.filter(item => item.active).map(item => item.name)'
          }
        ],
        codeQuality: {
          complexity: 7,
          maintainability: 85,
          testability: 78,
          readability: 82
        }
      }
      
      setAnalysis(mockAnalysis)
      onAnalysis?.(mockAnalysis)
    } catch (error) {
      console.error('Analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'bg-red-500'
      case 'medium': return 'bg-yellow-500'
      case 'low': return 'bg-blue-500'
      default: return 'bg-gray-500'
    }
  }

  return (
    <div className={cn('h-full flex flex-col', className)}>
      <Card className="flex-1 flex flex-col">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Code2 className="h-5 w-5" />
              Code Editor
            </CardTitle>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setActiveTab('editor')}
                className={cn(activeTab === 'editor' && 'bg-primary text-primary-foreground')}
              >
                <Code2 className="h-4 w-4 mr-1" />
                Editor
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setActiveTab('analysis')}
                className={cn(activeTab === 'analysis' && 'bg-primary text-primary-foreground')}
              >
                <Shield className="h-4 w-4 mr-1" />
                Analysis
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="flex-1 p-0">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="h-full">
            <TabsContent value="editor" className="h-full m-0">
              <div className="h-full flex flex-col">
                <div className="flex items-center justify-between p-3 border-b">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline">{language}</Badge>
                    <span className="text-sm text-muted-foreground">
                      {code.split('\n').length} lines
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      size="sm"
                      onClick={analyzeCode}
                      disabled={isAnalyzing}
                    >
                      {isAnalyzing ? (
                        <div className="animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full" />
                      ) : (
                        <Play className="h-4 w-4 mr-1" />
                      )}
                      {isAnalyzing ? 'Analyzing...' : 'Analyze Code'}
                    </Button>
                    <Button variant="outline" size="sm">
                      <Upload className="h-4 w-4 mr-1" />
                      Import
                    </Button>
                    <Button variant="outline" size="sm">
                      <Download className="h-4 w-4 mr-1" />
                      Export
                    </Button>
                  </div>
                </div>
                
                <div className="flex-1">
                  <Editor
                    height="100%"
                    language={language}
                    value={code}
                    onChange={handleCodeChange}
                    onMount={handleEditorDidMount}
                    theme="vs-dark"
                    options={{
                      minimap: { enabled: true },
                      fontSize: 14,
                      fontFamily: 'JetBrains Mono',
                      lineNumbers: 'on',
                      roundedSelection: false,
                      scrollBeyondLastLine: false,
                      automaticLayout: true,
                      wordWrap: 'on',
                      suggestOnTriggerCharacters: true,
                      quickSuggestions: true,
                      parameterHints: { enabled: true },
                      hover: { enabled: true },
                      contextmenu: true,
                      folding: true,
                      foldingStrategy: 'indentation',
                      showFoldingControls: 'always',
                      matchBrackets: 'always',
                      autoClosingBrackets: 'always',
                      autoClosingQuotes: 'always',
                      formatOnPaste: true,
                      formatOnType: true,
                    }}
                  />
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="analysis" className="h-full m-0">
              <div className="h-full flex flex-col">
                <div className="p-3 border-b">
                  <h3 className="font-semibold">AI Code Analysis</h3>
                  <p className="text-sm text-muted-foreground">
                    Security, performance, and refactoring insights
                  </p>
                </div>
                
                <div className="flex-1 overflow-auto p-4">
                  {analysis ? (
                    <div className="space-y-6">
                      {/* Code Quality Metrics */}
                      <div>
                        <h4 className="font-medium mb-3 flex items-center gap-2">
                          <Zap className="h-4 w-4" />
                          Code Quality Metrics
                        </h4>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                          {Object.entries(analysis.codeQuality).map(([key, value]) => (
                            <div key={key} className="text-center p-3 bg-muted rounded-lg">
                              <div className="text-2xl font-bold text-primary">{value}</div>
                              <div className="text-xs text-muted-foreground capitalize">
                                {key.replace(/([A-Z])/g, ' $1').trim()}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Security Issues */}
                      {analysis.securityIssues.length > 0 && (
                        <div>
                          <h4 className="font-medium mb-3 flex items-center gap-2">
                            <Shield className="h-4 w-4" />
                            Security Issues ({analysis.securityIssues.length})
                          </h4>
                          <div className="space-y-2">
                            {analysis.securityIssues.map((issue, index) => (
                              <div key={index} className="p-3 border rounded-lg">
                                <div className="flex items-center gap-2 mb-2">
                                  <div className={cn('w-3 h-3 rounded-full', getSeverityColor(issue.severity))} />
                                  <span className="font-medium">Line {issue.line}</span>
                                  <Badge variant="destructive">{issue.severity}</Badge>
                                </div>
                                <p className="text-sm mb-2">{issue.message}</p>
                                <p className="text-xs text-muted-foreground">
                                  <strong>Suggestion:</strong> {issue.suggestion}
                                </p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Performance Issues */}
                      {analysis.performanceIssues.length > 0 && (
                        <div>
                          <h4 className="font-medium mb-3 flex items-center gap-2">
                            <Zap className="h-4 w-4" />
                            Performance Issues ({analysis.performanceIssues.length})
                          </h4>
                          <div className="space-y-2">
                            {analysis.performanceIssues.map((issue, index) => (
                              <div key={index} className="p-3 border rounded-lg">
                                <div className="flex items-center gap-2 mb-2">
                                  <AlertTriangle className="h-4 w-4 text-yellow-500" />
                                  <span className="font-medium">Line {issue.line}</span>
                                  <Badge variant="secondary">{issue.impact} impact</Badge>
                                </div>
                                <p className="text-sm mb-2">{issue.message}</p>
                                <p className="text-xs text-muted-foreground">
                                  <strong>Optimization:</strong> {issue.optimization}
                                </p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Refactoring Suggestions */}
                      {analysis.refactoringSuggestions.length > 0 && (
                        <div>
                          <h4 className="font-medium mb-3 flex items-center gap-2">
                            <CheckCircle className="h-4 w-4" />
                            Refactoring Suggestions ({analysis.refactoringSuggestions.length})
                          </h4>
                          <div className="space-y-2">
                            {analysis.refactoringSuggestions.map((suggestion, index) => (
                              <div key={index} className="p-3 border rounded-lg">
                                <div className="flex items-center gap-2 mb-2">
                                  <span className="font-medium">Line {suggestion.line}</span>
                                  <Badge variant="outline">{suggestion.type}</Badge>
                                </div>
                                <p className="text-sm mb-2">{suggestion.message}</p>
                                <div className="text-xs space-y-1">
                                  <div>
                                    <strong>Before:</strong>
                                    <pre className="bg-muted p-2 rounded mt-1 overflow-x-auto">
                                      {suggestion.before}
                                    </pre>
                                  </div>
                                  <div>
                                    <strong>After:</strong>
                                    <pre className="bg-muted p-2 rounded mt-1 overflow-x-auto">
                                      {suggestion.after}
                                    </pre>
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <Code2 className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                      <p className="text-muted-foreground">
                        Click "Analyze Code" to get AI-powered insights
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}
