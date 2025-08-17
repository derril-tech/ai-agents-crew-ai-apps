'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  BarChart3, 
  PieChart,
  Activity,
  Target,
  AlertTriangle,
  ArrowUpRight,
  ArrowDownRight,
  RefreshCw,
  Settings
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart as RechartsPieChart, Cell } from 'recharts'
import { createChart, ColorType } from 'lightweight-charts'
import { cn } from '@/lib/utils'

interface FinancialData {
  timestamp: number
  value: number
  change: number
  changePercent: number
}

interface KPICard {
  title: string
  value: string
  change: number
  changePercent: number
  icon: React.ReactNode
  color: string
}

interface ChartData {
  name: string
  value: number
  color: string
}

export function FinancialDashboard() {
  const [timeframe, setTimeframe] = useState('1D')
  const [isLoading, setIsLoading] = useState(false)
  const [financialData, setFinancialData] = useState<FinancialData[]>([])
  const [selectedAsset, setSelectedAsset] = useState('BTC')

  // Mock KPI data
  const kpiData: KPICard[] = [
    {
      title: 'Portfolio Value',
      value: '$124,567.89',
      change: 2345.67,
      changePercent: 1.92,
      icon: <DollarSign className="h-5 w-5" />,
      color: 'text-green-600'
    },
    {
      title: 'Total Return',
      value: '+12.45%',
      change: 2.34,
      changePercent: 0.23,
      icon: <TrendingUp className="h-5 w-5" />,
      color: 'text-green-600'
    },
    {
      title: 'Risk Score',
      value: 'Medium',
      change: -0.5,
      changePercent: -2.1,
      icon: <AlertTriangle className="h-5 w-5" />,
      color: 'text-yellow-600'
    },
    {
      title: 'Sharpe Ratio',
      value: '1.85',
      change: 0.12,
      changePercent: 6.9,
      icon: <Target className="h-5 w-5" />,
      color: 'text-blue-600'
    }
  ]

  // Mock chart data
  const portfolioData = [
    { time: '2024-01-01', value: 100000 },
    { time: '2024-01-02', value: 102000 },
    { time: '2024-01-03', value: 101500 },
    { time: '2024-01-04', value: 103200 },
    { time: '2024-01-05', value: 104500 },
    { time: '2024-01-06', value: 106000 },
    { time: '2024-01-07', value: 105800 },
    { time: '2024-01-08', value: 107500 },
    { time: '2024-01-09', value: 108200 },
    { time: '2024-01-10', value: 110000 },
    { time: '2024-01-11', value: 112000 },
    { time: '2024-01-12', value: 111500 },
    { time: '2024-01-13', value: 113200 },
    { time: '2024-01-14', value: 114500 },
    { time: '2024-01-15', value: 116000 },
    { time: '2024-01-16', value: 117500 },
    { time: '2024-01-17', value: 118200 },
    { time: '2024-01-18', value: 120000 },
    { time: '2024-01-19', value: 122000 },
    { time: '2024-01-20', value: 121500 },
    { time: '2024-01-21', value: 123200 },
    { time: '2024-01-22', value: 124500 },
    { time: '2024-01-23', value: 126000 },
    { time: '2024-01-24', value: 124567 }
  ]

  const assetAllocation: ChartData[] = [
    { name: 'Stocks', value: 45, color: '#3B82F6' },
    { name: 'Bonds', value: 25, color: '#10B981' },
    { name: 'Crypto', value: 15, color: '#F59E0B' },
    { name: 'Real Estate', value: 10, color: '#EF4444' },
    { name: 'Cash', value: 5, color: '#8B5CF6' }
  ]

  const sectorPerformance = [
    { name: 'Technology', value: 125000, change: 5.2 },
    { name: 'Healthcare', value: 85000, change: 2.1 },
    { name: 'Finance', value: 95000, change: -1.8 },
    { name: 'Energy', value: 65000, change: 3.4 },
    { name: 'Consumer', value: 75000, change: 1.2 }
  ]

  useEffect(() => {
    // Initialize lightweight chart
    const chartContainer = document.getElementById('trading-chart')
    if (chartContainer) {
      const chart = createChart(chartContainer, {
        layout: {
          background: { type: ColorType.Solid, color: 'transparent' },
          textColor: '#9CA3AF',
        },
        grid: {
          vertLines: { color: '#374151' },
          horzLines: { color: '#374151' },
        },
        width: chartContainer.clientWidth,
        height: 300,
      })

      const lineSeries = chart.addLineSeries({
        color: '#3B82F6',
        lineWidth: 2,
      })

      lineSeries.setData(portfolioData.map(item => ({
        time: item.time,
        value: item.value
      })))

      const handleResize = () => {
        chart.applyOptions({ width: chartContainer.clientWidth })
      }

      window.addEventListener('resize', handleResize)

      return () => {
        window.removeEventListener('resize', handleResize)
        chart.remove()
      }
    }
  }, [])

  const refreshData = () => {
    setIsLoading(true)
    // Simulate data refresh
    setTimeout(() => setIsLoading(false), 1000)
  }

  const getChangeIcon = (change: number) => {
    return change >= 0 ? (
      <ArrowUpRight className="h-4 w-4 text-green-500" />
    ) : (
      <ArrowDownRight className="h-4 w-4 text-red-500" />
    )
  }

  const getChangeColor = (change: number) => {
    return change >= 0 ? 'text-green-600' : 'text-red-600'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Financial Analytics Dashboard</h1>
          <p className="text-muted-foreground">
            Real-time portfolio analysis and market insights
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
        {kpiData.map((kpi, index) => (
          <Card key={index}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {kpi.title}
              </CardTitle>
              <div className={cn("p-2 rounded-lg", kpi.color.replace('text-', 'bg-').replace('-600', '-100'))}>
                {kpi.icon}
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{kpi.value}</div>
              <div className="flex items-center gap-1 text-xs">
                {getChangeIcon(kpi.change)}
                <span className={getChangeColor(kpi.change)}>
                  {kpi.change >= 0 ? '+' : ''}{kpi.changePercent.toFixed(2)}%
                </span>
                <span className="text-muted-foreground">
                  from last period
                </span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Dashboard */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Portfolio Overview</TabsTrigger>
          <TabsTrigger value="analysis">AI Analysis</TabsTrigger>
          <TabsTrigger value="trading">Trading View</TabsTrigger>
          <TabsTrigger value="reports">Reports</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Portfolio Performance Chart */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Portfolio Performance
                </CardTitle>
                <div className="flex items-center gap-2">
                  {['1D', '1W', '1M', '3M', '1Y', 'ALL'].map((period) => (
                    <Button
                      key={period}
                      variant={timeframe === period ? "default" : "outline"}
                      size="sm"
                      onClick={() => setTimeframe(period)}
                    >
                      {period}
                    </Button>
                  ))}
                </div>
              </CardHeader>
              <CardContent>
                <div id="trading-chart" className="w-full h-[300px]" />
              </CardContent>
            </Card>

            {/* Asset Allocation */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <PieChart className="h-5 w-5" />
                  Asset Allocation
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <RechartsPieChart>
                    {assetAllocation.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </RechartsPieChart>
                </ResponsiveContainer>
                <div className="space-y-2 mt-4">
                  {assetAllocation.map((asset, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div 
                          className="w-3 h-3 rounded-full" 
                          style={{ backgroundColor: asset.color }}
                        />
                        <span className="text-sm">{asset.name}</span>
                      </div>
                      <span className="text-sm font-medium">{asset.value}%</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sector Performance */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Sector Performance
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={sectorPerformance}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#3B82F6" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analysis" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* AI Insights */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="h-5 w-5" />
                  AI Market Insights
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="p-4 bg-blue-50 rounded-lg">
                    <h4 className="font-medium text-blue-900 mb-2">Market Sentiment</h4>
                    <p className="text-sm text-blue-700">
                      AI analysis indicates bullish sentiment for technology stocks. 
                      Consider increasing exposure to tech sector by 5-10%.
                    </p>
                  </div>
                  <div className="p-4 bg-green-50 rounded-lg">
                    <h4 className="font-medium text-green-900 mb-2">Risk Assessment</h4>
                    <p className="text-sm text-green-700">
                      Portfolio risk level is optimal. Current diversification 
                      provides good protection against market volatility.
                    </p>
                  </div>
                  <div className="p-4 bg-yellow-50 rounded-lg">
                    <h4 className="font-medium text-yellow-900 mb-2">Opportunity Alert</h4>
                    <p className="text-sm text-yellow-700">
                      Emerging markets showing strong momentum. Consider 
                      allocating 3-5% to emerging market ETFs.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Performance Metrics */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5" />
                  Performance Metrics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Sharpe Ratio</span>
                    <Badge variant="outline">1.85</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Beta</span>
                    <Badge variant="outline">0.92</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Alpha</span>
                    <Badge variant="outline">2.34%</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Max Drawdown</span>
                    <Badge variant="outline">-8.5%</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Volatility</span>
                    <Badge variant="outline">12.3%</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="trading" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Trading View</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Advanced trading interface with real-time charts and order management.
              </p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="reports" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Financial Reports</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Generate and download comprehensive financial reports and analysis.
              </p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
