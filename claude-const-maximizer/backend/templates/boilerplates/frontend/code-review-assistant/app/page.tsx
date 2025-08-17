'use client'

import { useState } from 'react'
import { CodeEditor } from '@/components/code-editor/CodeEditor'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Code2, 
  Shield, 
  Zap, 
  Users, 
  Settings, 
  FileText,
  GitBranch,
  History,
  Plus,
  FolderOpen
} from 'lucide-react'

interface Project {
  id: string
  name: string
  language: string
  lastModified: string
  issues: number
  status: 'clean' | 'warnings' | 'critical'
}

export default function CodeReviewAssistant() {
  const [activeProject, setActiveProject] = useState<string | null>(null)
  const [projects] = useState<Project[]>([
    {
      id: '1',
      name: 'main.tsx',
      language: 'typescript',
      lastModified: '2 hours ago',
      issues: 3,
      status: 'warnings'
    },
    {
      id: '2',
      name: 'api.ts',
      language: 'typescript',
      lastModified: '1 day ago',
      issues: 0,
      status: 'clean'
    },
    {
      id: '3',
      name: 'utils.js',
      language: 'javascript',
      lastModified: '3 days ago',
      issues: 7,
      status: 'critical'
    }
  ])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'clean': return 'bg-green-500'
      case 'warnings': return 'bg-yellow-500'
      case 'critical': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'clean': return 'Clean'
      case 'warnings': return 'Warnings'
      case 'critical': return 'Critical'
      default: return 'Unknown'
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-14 items-center">
          <div className="flex items-center gap-2">
            <Code2 className="h-6 w-6 text-primary" />
            <h1 className="text-lg font-semibold">AI Code Review Assistant</h1>
          </div>
          
          <div className="ml-auto flex items-center gap-2">
            <Button variant="outline" size="sm">
              <GitBranch className="h-4 w-4 mr-1" />
              Connect Repository
            </Button>
            <Button variant="outline" size="sm">
              <Settings className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100vh-8rem)]">
          {/* Sidebar - Project Explorer */}
          <div className="lg:col-span-1">
            <Card className="h-full">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-sm">Project Explorer</CardTitle>
                  <Button size="sm" variant="outline">
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="p-0">
                <div className="space-y-1">
                  {projects.map((project) => (
                    <div
                      key={project.id}
                      className={`p-3 cursor-pointer hover:bg-muted/50 transition-colors ${
                        activeProject === project.id ? 'bg-muted' : ''
                      }`}
                      onClick={() => setActiveProject(project.id)}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <FileText className="h-4 w-4 text-muted-foreground" />
                          <span className="text-sm font-medium">{project.name}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Badge variant="outline" className="text-xs">
                            {project.language}
                          </Badge>
                          <div className={`w-2 h-2 rounded-full ${getStatusColor(project.status)}`} />
                        </div>
                      </div>
                      <div className="flex items-center justify-between mt-1">
                        <span className="text-xs text-muted-foreground">
                          {project.lastModified}
                        </span>
                        {project.issues > 0 && (
                          <Badge variant="secondary" className="text-xs">
                            {project.issues} issues
                          </Badge>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Content - Code Editor */}
          <div className="lg:col-span-2">
            <CodeEditor
              initialValue={`// AI Code Review Assistant - Sample Code
import React, { useState, useEffect } from 'react'

interface User {
  id: string
  name: string
  email: string
  role: 'admin' | 'user'
}

function UserManagement() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/users')
      const data = await response.json()
      setUsers(data)
    } catch (err) {
      setError('Failed to fetch users')
    } finally {
      setLoading(false)
    }
  }

  const addUser = async (userData: Omit<User, 'id'>) => {
    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      })
      const newUser = await response.json()
      setUsers(prev => [...prev, newUser])
    } catch (err) {
      setError('Failed to add user')
    }
  }

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div>
      <h1>User Management</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name} ({user.email})</li>
        ))}
      </ul>
    </div>
  )
}

export default UserManagement`}
              language="typescript"
              onCodeChange={(value) => console.log('Code changed:', value)}
              onAnalysis={(analysis) => console.log('Analysis:', analysis)}
            />
          </div>

          {/* Right Sidebar - Analysis & History */}
          <div className="lg:col-span-1">
            <div className="space-y-6">
              {/* Quick Stats */}
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm">Quick Stats</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Total Issues</span>
                    <Badge variant="destructive">10</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Security</span>
                    <Badge variant="destructive">3</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Performance</span>
                    <Badge variant="secondary">5</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Code Quality</span>
                    <Badge variant="outline">2</Badge>
                  </div>
                </CardContent>
              </Card>

              {/* Recent Analysis */}
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm">Recent Analysis</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-xs">
                      <History className="h-3 w-3 text-muted-foreground" />
                      <span>main.tsx - 2 hours ago</span>
                    </div>
                    <div className="flex items-center gap-2 text-xs">
                      <History className="h-3 w-3 text-muted-foreground" />
                      <span>api.ts - 1 day ago</span>
                    </div>
                    <div className="flex items-center gap-2 text-xs">
                      <History className="h-3 w-3 text-muted-foreground" />
                      <span>utils.js - 3 days ago</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* AI Suggestions */}
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm">AI Suggestions</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="p-2 bg-muted rounded text-xs">
                      <strong>Security:</strong> Consider using parameterized queries
                    </div>
                    <div className="p-2 bg-muted rounded text-xs">
                      <strong>Performance:</strong> Optimize the user fetch loop
                    </div>
                    <div className="p-2 bg-muted rounded text-xs">
                      <strong>Quality:</strong> Extract error handling logic
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
