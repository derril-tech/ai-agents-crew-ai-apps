'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  TrendingUp, 
  ShoppingCart, 
  DollarSign, 
  Users, 
  Package,
  Eye,
  Star,
  RefreshCw,
  Settings,
  BarChart3,
  PieChart,
  LineChart,
  Activity
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart as RechartsPieChart, Cell, AreaChart, Area } from 'recharts'
import { cn } from '@/lib/utils'

interface SalesData {
  date: string
  revenue: number
  orders: number
  customers: number
  conversionRate: number
}

interface ProductData {
  id: string
  name: string
  category: string
  price: number
  stock: number
  sales: number
  rating: number
  status: 'in_stock' | 'low_stock' | 'out_of_stock'
}

interface CustomerData {
  id: string
  name: string
  email: string
  totalSpent: number
  orders: number
  lastPurchase: string
  segment: 'vip' | 'regular' | 'new'
}

export function EcommerceDashboard() {
  const [activeTab, setActiveTab] = useState('overview')
  const [isLoading, setIsLoading] = useState(false)
  const [timeframe, setTimeframe] = useState('7d')

  // Mock sales data
  const salesData: SalesData[] = [
    { date: '2024-01-01', revenue: 12500, orders: 45, customers: 38, conversionRate: 3.2 },
    { date: '2024-01-02', revenue: 14200, orders: 52, customers: 44, conversionRate: 3.8 },
    { date: '2024-01-03', revenue: 11800, orders: 41, customers: 35, conversionRate: 2.9 },
    { date: '2024-01-04', revenue: 15600, orders: 58, customers: 49, conversionRate: 4.1 },
    { date: '2024-01-05', revenue: 16800, orders: 62, customers: 53, conversionRate: 4.3 },
    { date: '2024-01-06', revenue: 18900, orders: 71, customers: 61, conversionRate: 4.8 },
    { date: '2024-01-07', revenue: 20100, orders: 78, customers: 67, conversionRate: 5.2 }
  ]

  // Mock product data
  const products: ProductData[] = [
    { id: '1', name: 'Wireless Headphones', category: 'Electronics', price: 199.99, stock: 45, sales: 23, rating: 4.5, status: 'in_stock' },
    { id: '2', name: 'Smart Watch', category: 'Electronics', price: 299.99, stock: 12, sales: 18, rating: 4.8, status: 'low_stock' },
    { id: '3', name: 'Running Shoes', category: 'Sports', price: 89.99, stock: 0, sales: 34, rating: 4.2, status: 'out_of_stock' },
    { id: '4', name: 'Coffee Maker', category: 'Home', price: 149.99, stock: 28, sales: 15, rating: 4.6, status: 'in_stock' },
    { id: '5', name: 'Yoga Mat', category: 'Sports', price: 29.99, stock: 67, sales: 42, rating: 4.3, status: 'in_stock' }
  ]

  // Mock customer data
  const customers: CustomerData[] = [
    { id: '1', name: 'John Smith', email: 'john@example.com', totalSpent: 1250.50, orders: 8, lastPurchase: '2024-01-05', segment: 'vip' },
    { id: '2', name: 'Sarah Johnson', email: 'sarah@example.com', totalSpent: 890.25, orders: 6, lastPurchase: '2024-01-03', segment: 'regular' },
    { id: '3', name: 'Mike Brown', email: 'mike@example.com', totalSpent: 450.75, orders: 3, lastPurchase: '2024-01-06', segment: 'new' },
    { id: '4', name: 'Lisa Davis', email: 'lisa@example.com', totalSpent: 2100.00, orders: 12, lastPurchase: '2024-01-07', segment: 'vip' }
  ]

  const categoryData = [
    { name: 'Electronics', value: 45, color: '#3B82F6' },
    { name: 'Sports', value: 25, color: '#10B981' },
    { name: 'Home', value: 20, color: '#F59E0B' },
    { name: 'Fashion', value: 10, color: '#EF4444' }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'in_stock': return 'bg-green-500'
      case 'low_stock': return 'bg-yellow-500'
      case 'out_of_stock': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  const getSegmentColor = (segment: string) => {
    switch (segment) {
      case 'vip': return 'bg-purple-500'
      case 'regular': return 'bg-blue-500'
      case 'new': return 'bg-green-500'
      default: return 'bg-gray-500'
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
          <h1 className="text-2xl font-bold">E-commerce Analytics Dashboard</h1>
          <p className="text-muted-foreground">
            Real-time sales tracking and business insights
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
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$109,900</div>
            <p className="text-xs text-muted-foreground">
              +12.5% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Orders</CardTitle>
            <ShoppingCart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">4,207</div>
            <p className="text-xs text-muted-foreground">
              +8.2% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Customers</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3,847</div>
            <p className="text-xs text-muted-foreground">
              +15.3% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">4.1%</div>
            <p className="text-xs text-muted-foreground">
              +0.8% from last month
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Dashboard */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="products">Products</TabsTrigger>
          <TabsTrigger value="customers">Customers</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Sales Chart */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Sales Performance
                </CardTitle>
                <div className="flex items-center gap-2">
                  {['7d', '30d', '90d', '1y'].map((period) => (
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
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={salesData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="revenue" stroke="#3B82F6" fill="#DBEAFE" />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Category Distribution */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <PieChart className="h-5 w-5" />
                  Sales by Category
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <RechartsPieChart>
                    {categoryData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </RechartsPieChart>
                </ResponsiveContainer>
                <div className="space-y-2 mt-4">
                  {categoryData.map((category, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div 
                          className="w-3 h-3 rounded-full" 
                          style={{ backgroundColor: category.color }}
                        />
                        <span className="text-sm">{category.name}</span>
                      </div>
                      <span className="text-sm font-medium">{category.value}%</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="products" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Package className="h-5 w-5" />
                Product Inventory
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {products.map((product) => (
                  <div
                    key={product.id}
                    className="flex items-center justify-between p-4 border rounded-lg"
                  >
                    <div className="flex items-center gap-4">
                      <div className={`w-3 h-3 rounded-full ${getStatusColor(product.status)}`} />
                      <div>
                        <h4 className="font-medium">{product.name}</h4>
                        <p className="text-sm text-muted-foreground">
                          {product.category} • ${product.price}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-6">
                      <div className="text-center">
                        <p className="text-sm text-muted-foreground">Stock</p>
                        <p className="font-medium">{product.stock}</p>
                      </div>
                      <div className="text-center">
                        <p className="text-sm text-muted-foreground">Sales</p>
                        <p className="font-medium">{product.sales}</p>
                      </div>
                      <div className="text-center">
                        <p className="text-sm text-muted-foreground">Rating</p>
                        <div className="flex items-center gap-1">
                          <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                          <span className="text-sm font-medium">{product.rating}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="customers" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                Customer Insights
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {customers.map((customer) => (
                  <div
                    key={customer.id}
                    className="flex items-center justify-between p-4 border rounded-lg"
                  >
                    <div className="flex items-center gap-4">
                      <div className={`w-3 h-3 rounded-full ${getSegmentColor(customer.segment)}`} />
                      <div>
                        <h4 className="font-medium">{customer.name}</h4>
                        <p className="text-sm text-muted-foreground">
                          {customer.email} • {customer.segment.toUpperCase()}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-6">
                      <div className="text-center">
                        <p className="text-sm text-muted-foreground">Total Spent</p>
                        <p className="font-medium">${customer.totalSpent.toFixed(2)}</p>
                      </div>
                      <div className="text-center">
                        <p className="text-sm text-muted-foreground">Orders</p>
                        <p className="font-medium">{customer.orders}</p>
                      </div>
                      <div className="text-center">
                        <p className="text-sm text-muted-foreground">Last Purchase</p>
                        <p className="font-medium">{customer.lastPurchase}</p>
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
            {/* Conversion Funnel */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="h-5 w-5" />
                  Conversion Funnel
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={[
                    { stage: 'Visitors', count: 10000, conversion: 100 },
                    { stage: 'Add to Cart', count: 2500, conversion: 25 },
                    { stage: 'Checkout', count: 1000, conversion: 10 },
                    { stage: 'Purchase', count: 410, conversion: 4.1 }
                  ]}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="stage" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="conversion" fill="#3B82F6" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Customer Segments */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  Customer Segments
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={[
                    { segment: 'VIP', customers: 450, revenue: 67500 },
                    { segment: 'Regular', customers: 2100, revenue: 315000 },
                    { segment: 'New', customers: 1297, revenue: 64850 }
                  ]}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="segment" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="customers" fill="#10B981" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
