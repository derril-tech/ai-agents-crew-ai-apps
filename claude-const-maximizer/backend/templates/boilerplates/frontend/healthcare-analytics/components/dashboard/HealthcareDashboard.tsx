'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Activity, 
  Users, 
  Heart, 
  Stethoscope, 
  TrendingUp, 
  AlertTriangle,
  CheckCircle,
  Clock,
  Calendar,
  BarChart3,
  PieChart,
  LineChart,
  RefreshCw,
  Settings
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart as RechartsPieChart, Cell, AreaChart, Area } from 'recharts'
import { cn } from '@/lib/utils'

interface PatientData {
  id: string
  name: string
  age: number
  status: 'stable' | 'critical' | 'improving' | 'monitoring'
  vitalSigns: {
    heartRate: number
    bloodPressure: string
    temperature: number
    oxygenSaturation: number
  }
  lastUpdate: string
}

interface VitalSignsData {
  time: string
  heartRate: number
  bloodPressureSystolic: number
  bloodPressureDiastolic: number
  temperature: number
  oxygenSaturation: number
}

export function HealthcareDashboard() {
  const [activeTab, setActiveTab] = useState('overview')
  const [isLoading, setIsLoading] = useState(false)
  const [selectedPatient, setSelectedPatient] = useState<string | null>(null)

  // Mock patient data
  const patients: PatientData[] = [
    {
      id: '1',
      name: 'John Smith',
      age: 45,
      status: 'stable',
      vitalSigns: {
        heartRate: 72,
        bloodPressure: '120/80',
        temperature: 98.6,
        oxygenSaturation: 98
      },
      lastUpdate: '2 minutes ago'
    },
    {
      id: '2',
      name: 'Sarah Johnson',
      age: 32,
      status: 'critical',
      vitalSigns: {
        heartRate: 110,
        bloodPressure: '140/95',
        temperature: 101.2,
        oxygenSaturation: 92
      },
      lastUpdate: '1 minute ago'
    },
    {
      id: '3',
      name: 'Michael Brown',
      age: 58,
      status: 'improving',
      vitalSigns: {
        heartRate: 68,
        bloodPressure: '118/78',
        temperature: 98.8,
        oxygenSaturation: 96
      },
      lastUpdate: '5 minutes ago'
    }
  ]

  // Mock vital signs data
  const vitalSignsData: VitalSignsData[] = [
    { time: '00:00', heartRate: 72, bloodPressureSystolic: 120, bloodPressureDiastolic: 80, temperature: 98.6, oxygenSaturation: 98 },
    { time: '02:00', heartRate: 70, bloodPressureSystolic: 118, bloodPressureDiastolic: 78, temperature: 98.4, oxygenSaturation: 97 },
    { time: '04:00', heartRate: 75, bloodPressureSystolic: 122, bloodPressureDiastolic: 82, temperature: 98.8, oxygenSaturation: 96 },
    { time: '06:00', heartRate: 68, bloodPressureSystolic: 115, bloodPressureDiastolic: 75, temperature: 98.2, oxygenSaturation: 98 },
    { time: '08:00', heartRate: 80, bloodPressureSystolic: 125, bloodPressureDiastolic: 85, temperature: 99.0, oxygenSaturation: 95 },
    { time: '10:00', heartRate: 85, bloodPressureSystolic: 130, bloodPressureDiastolic: 88, temperature: 99.2, oxygenSaturation: 94 },
    { time: '12:00', heartRate: 78, bloodPressureSystolic: 120, bloodPressureDiastolic: 80, temperature: 98.6, oxygenSaturation: 97 },
    { time: '14:00', heartRate: 72, bloodPressureSystolic: 118, bloodPressureDiastolic: 78, temperature: 98.4, oxygenSaturation: 98 },
    { time: '16:00', heartRate: 70, bloodPressureSystolic: 115, bloodPressureDiastolic: 75, temperature: 98.2, oxygenSaturation: 99 },
    { time: '18:00', heartRate: 75, bloodPressureSystolic: 122, bloodPressureDiastolic: 82, temperature: 98.8, oxygenSaturation: 96 },
    { time: '20:00', heartRate: 68, bloodPressureSystolic: 118, bloodPressureDiastolic: 78, temperature: 98.4, oxygenSaturation: 97 },
    { time: '22:00', heartRate: 72, bloodPressureSystolic: 120, bloodPressureDiastolic: 80, temperature: 98.6, oxygenSaturation: 98 }
  ]

  const departmentStats = [
    { name: 'Emergency', patients: 12, occupancy: 85, color: '#EF4444' },
    { name: 'ICU', patients: 8, occupancy: 100, color: '#F59E0B' },
    { name: 'Cardiology', patients: 15, occupancy: 75, color: '#3B82F6' },
    { name: 'Neurology', patients: 10, occupancy: 60, color: '#10B981' },
    { name: 'Pediatrics', patients: 20, occupancy: 80, color: '#8B5CF6' }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'stable': return 'bg-green-500'
      case 'critical': return 'bg-red-500'
      case 'improving': return 'bg-blue-500'
      case 'monitoring': return 'bg-yellow-500'
      default: return 'bg-gray-500'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'stable': return 'Stable'
      case 'critical': return 'Critical'
      case 'improving': return 'Improving'
      case 'monitoring': return 'Monitoring'
      default: return 'Unknown'
    }
  }

  const refreshData = () => {
    setIsLoading(true)
    setTimeout(() => setIsLoading(false), 1000)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Healthcare Analytics Dashboard</h1>
          <p className="text-muted-foreground">
            Real-time patient monitoring and medical analytics
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={refreshData}
            disabled={isLoading}
          >
            <RefreshCw className={cn("h-4 w-4 mr-1", isLoading && "animate-spin")} />
            Refresh
          </Button>
          <Button variant="outline" size="sm">
            <Settings className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Patients</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1,247</div>
            <p className="text-xs text-muted-foreground">
              +12% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Critical Cases</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">23</div>
            <p className="text-xs text-muted-foreground">
              -5% from yesterday
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Recovery Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">94.2%</div>
            <p className="text-xs text-muted-foreground">
              +2.1% from last week
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Wait Time</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">18 min</div>
            <p className="text-xs text-muted-foreground">
              -3 min from yesterday
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Dashboard */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="patients">Patient Monitoring</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="departments">Departments</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Vital Signs Chart */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="h-5 w-5" />
                  Vital Signs Trends
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={vitalSignsData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="heartRate" stroke="#EF4444" fill="#FEE2E2" />
                    <Area type="monotone" dataKey="oxygenSaturation" stroke="#10B981" fill="#D1FAE5" />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Patient Status */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Patient Status
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <RechartsPieChart>
                    <Cell key="stable" fill="#10B981" />
                    <Cell key="critical" fill="#EF4444" />
                    <Cell key="improving" fill="#3B82F6" />
                    <Cell key="monitoring" fill="#F59E0B" />
                  </RechartsPieChart>
                </ResponsiveContainer>
                <div className="space-y-2 mt-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-green-500" />
                      <span className="text-sm">Stable</span>
                    </div>
                    <span className="text-sm font-medium">1,180</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-red-500" />
                      <span className="text-sm">Critical</span>
                    </div>
                    <span className="text-sm font-medium">23</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-blue-500" />
                      <span className="text-sm">Improving</span>
                    </div>
                    <span className="text-sm font-medium">32</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-yellow-500" />
                      <span className="text-sm">Monitoring</span>
                    </div>
                    <span className="text-sm font-medium">12</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="patients" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Stethoscope className="h-5 w-5" />
                Active Patient Monitoring
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {patients.map((patient) => (
                  <div
                    key={patient.id}
                    className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                      selectedPatient === patient.id ? 'border-primary bg-primary/5' : 'hover:bg-muted/50'
                    }`}
                    onClick={() => setSelectedPatient(patient.id)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className={`w-3 h-3 rounded-full ${getStatusColor(patient.status)}`} />
                        <div>
                          <h4 className="font-medium">{patient.name}</h4>
                          <p className="text-sm text-muted-foreground">
                            Age {patient.age} • {getStatusText(patient.status)}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-medium">{patient.vitalSigns.heartRate} bpm</p>
                        <p className="text-xs text-muted-foreground">{patient.lastUpdate}</p>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-4 gap-4 mt-3">
                      <div className="text-center">
                        <p className="text-xs text-muted-foreground">Heart Rate</p>
                        <p className="font-medium">{patient.vitalSigns.heartRate} bpm</p>
                      </div>
                      <div className="text-center">
                        <p className="text-xs text-muted-foreground">Blood Pressure</p>
                        <p className="font-medium">{patient.vitalSigns.bloodPressure}</p>
                      </div>
                      <div className="text-center">
                        <p className="text-xs text-muted-foreground">Temperature</p>
                        <p className="font-medium">{patient.vitalSigns.temperature}°F</p>
                      </div>
                      <div className="text-center">
                        <p className="text-xs text-muted-foreground">O₂ Sat</p>
                        <p className="font-medium">{patient.vitalSigns.oxygenSaturation}%</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Department Performance */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  Department Performance
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={departmentStats}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="patients" fill="#3B82F6" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Patient Flow */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Patient Flow Trends
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={vitalSignsData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="heartRate" stroke="#EF4444" strokeWidth={2} />
                    <Line type="monotone" dataKey="oxygenSaturation" stroke="#10B981" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="departments" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {departmentStats.map((dept, index) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle className="text-sm">{dept.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Patients</span>
                      <span className="font-medium">{dept.patients}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Occupancy</span>
                      <span className="font-medium">{dept.occupancy}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="h-2 rounded-full"
                        style={{
                          width: `${dept.occupancy}%`,
                          backgroundColor: dept.color
                        }}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
