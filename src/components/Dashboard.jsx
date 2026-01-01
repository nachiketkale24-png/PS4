import React, { useState } from 'react';
import { 
  LayoutDashboard, 
  MapPin, 
  Droplets, 
  BarChart3, 
  MessageSquare,
  Bell,
  Search,
  Menu,
  X,
  Sprout,
  TrendingUp,
  AlertCircle,
  CloudRain,
  Thermometer,
  Wind,
  Calendar,
  Settings,
  User,
  ChevronRight,
  Activity,
  Zap,
  Award
} from 'lucide-react';
import AssistantBubble from './AssistantBubble';

const Dashboard = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeNav, setActiveNav] = useState('dashboard');

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'fields', label: 'Fields', icon: MapPin },
    { id: 'irrigation', label: 'Irrigation', icon: Droplets },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'assistant', label: 'Chat Assistant', icon: MessageSquare },
  ];

  const kpis = [
    {
      title: 'Water Saved',
      value: '2,847 L',
      change: '+12.5%',
      trend: 'up',
      icon: Droplets,
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'bg-blue-50',
    },
    {
      title: 'Estimated Yield',
      value: '4.2 tons',
      change: '+8.3%',
      trend: 'up',
      icon: Sprout,
      color: 'from-green-500 to-emerald-500',
      bgColor: 'bg-green-50',
    },
    {
      title: 'Active Alerts',
      value: '3',
      change: '-2 from yesterday',
      trend: 'down',
      icon: AlertCircle,
      color: 'from-amber-500 to-orange-500',
      bgColor: 'bg-amber-50',
    },
    {
      title: 'Energy Efficiency',
      value: '94%',
      change: '+3.2%',
      trend: 'up',
      icon: Zap,
      color: 'from-purple-500 to-pink-500',
      bgColor: 'bg-purple-50',
    },
  ];

  const alerts = [
    {
      id: 1,
      type: 'warning',
      title: 'Low soil moisture detected',
      field: 'North Field A',
      time: '15 mins ago',
      urgent: true,
    },
    {
      id: 2,
      type: 'info',
      title: 'Optimal irrigation time',
      field: 'South Field B',
      time: '1 hour ago',
      urgent: false,
    },
    {
      id: 3,
      type: 'success',
      title: 'Irrigation completed',
      field: 'East Field C',
      time: '2 hours ago',
      urgent: false,
    },
  ];

  const weatherData = {
    temp: '28°C',
    condition: 'Partly Cloudy',
    humidity: '65%',
    wind: '12 km/h',
    precipitation: '20%',
  };

  const recommendations = [
    {
      id: 1,
      title: 'Irrigation Schedule',
      description: 'Schedule watering for North Field A in next 2 hours based on soil moisture levels',
      priority: 'high',
      time: '2:00 PM - 4:00 PM',
    },
    {
      id: 2,
      title: 'Fertilizer Application',
      description: 'NPK 19-19-19 recommended for South Field B to boost vegetative growth',
      priority: 'medium',
      time: 'This week',
    },
    {
      id: 3,
      title: 'Pest Monitoring',
      description: 'Increased pest activity predicted. Schedule inspection for all fields',
      priority: 'medium',
      time: 'Next 3 days',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-cream-50 via-white to-primary-50">
      {/* Header */}
      <header className="sticky top-0 z-40 backdrop-blur-xl bg-white/80 border-b border-sage-200/50 shadow-soft">
        <div className="flex items-center justify-between px-4 lg:px-8 py-4">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="lg:hidden p-2 hover:bg-sage-100 rounded-xl transition-colors"
            >
              {sidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
            
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center shadow-lg">
                <Sprout className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-sage-900">AgroSmart</h1>
                <p className="text-xs text-sage-600 hidden sm:block">Intelligent Farm Management</p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden md:flex items-center gap-2 bg-sage-50 rounded-2xl px-4 py-2 border border-sage-200">
              <Search className="w-4 h-4 text-sage-500" />
              <input
                type="text"
                placeholder="Search fields, reports..."
                className="bg-transparent outline-none text-sm w-64 text-sage-700 placeholder:text-sage-400"
              />
            </div>

            <button className="relative p-2 hover:bg-sage-100 rounded-xl transition-colors">
              <Bell className="w-5 h-5 text-sage-700" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>

            <div className="flex items-center gap-3 pl-3 border-l border-sage-200">
              <div className="hidden sm:block text-right">
                <p className="text-sm font-semibold text-sage-900">Rajesh Kumar</p>
                <p className="text-xs text-sage-600">Farm Owner</p>
              </div>
              <div className="w-10 h-10 bg-gradient-to-br from-primary-400 to-primary-600 rounded-xl flex items-center justify-center text-white font-semibold shadow-lg">
                RK
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside
          className={`fixed lg:sticky top-0 left-0 h-screen bg-white/60 backdrop-blur-xl border-r border-sage-200/50 transition-transform duration-300 z-30 ${
            sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
          } w-64`}
        >
          <div className="p-6 pt-24 lg:pt-6">
            <nav className="space-y-2">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = activeNav === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => {
                      setActiveNav(item.id);
                      setSidebarOpen(false);
                    }}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all group ${
                      isActive
                        ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg shadow-primary-500/30'
                        : 'hover:bg-sage-50 text-sage-700'
                    }`}
                  >
                    <Icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-sage-600 group-hover:text-primary-600'}`} />
                    <span className="font-medium">{item.label}</span>
                    {isActive && <ChevronRight className="w-4 h-4 ml-auto" />}
                  </button>
                );
              })}
            </nav>

            <div className="mt-8 p-4 bg-gradient-to-br from-primary-50 to-cream-100 rounded-2xl border border-primary-200/50">
              <Award className="w-8 h-8 text-primary-600 mb-2" />
              <h3 className="font-semibold text-sage-900 mb-1">Premium Plan</h3>
              <p className="text-xs text-sage-600 mb-3">Unlock advanced analytics and AI insights</p>
              <button className="w-full bg-gradient-to-r from-primary-500 to-primary-600 text-white px-4 py-2 rounded-xl text-sm font-medium hover:shadow-lg transition-shadow">
                Upgrade Now
              </button>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-4 lg:p-8 space-y-6">
          {/* Welcome Section */}
          <div className="mb-6">
            <h2 className="text-3xl font-bold text-sage-900 mb-2">Welcome back, Rajesh! 👋</h2>
            <p className="text-sage-600">Here's what's happening with your farm today.</p>
          </div>

          {/* KPI Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {kpis.map((kpi, index) => {
              const Icon = kpi.icon;
              return (
                <div
                  key={index}
                  className="group relative overflow-hidden bg-white/70 backdrop-blur-md rounded-2xl p-6 border border-sage-200/50 hover:shadow-depth transition-all duration-300 hover:-translate-y-1"
                >
                  <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br opacity-5 rounded-full -mr-16 -mt-16" 
                       style={{ background: `linear-gradient(135deg, var(--tw-gradient-stops))` }}></div>
                  
                  <div className={`w-12 h-12 ${kpi.bgColor} rounded-2xl flex items-center justify-center mb-4`}>
                    <Icon className={`w-6 h-6 bg-gradient-to-br ${kpi.color} bg-clip-text text-transparent`} style={{ WebkitTextFillColor: 'transparent' }} />
                  </div>

                  <div className="relative z-10">
                    <p className="text-sage-600 text-sm font-medium mb-1">{kpi.title}</p>
                    <p className="text-3xl font-bold text-sage-900 mb-2">{kpi.value}</p>
                    <div className="flex items-center gap-1">
                      <TrendingUp className={`w-4 h-4 ${kpi.trend === 'up' ? 'text-green-600' : 'text-red-600'}`} />
                      <span className={`text-sm font-semibold ${kpi.trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                        {kpi.change}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Live Field Map Placeholder */}
            <div className="lg:col-span-2 bg-white/70 backdrop-blur-md rounded-2xl p-6 border border-sage-200/50 shadow-soft">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold text-sage-900">Live Field Monitor</h3>
                  <p className="text-sm text-sage-600">Real-time satellite imagery and sensor data</p>
                </div>
                <button className="px-4 py-2 bg-sage-100 hover:bg-sage-200 rounded-xl text-sm font-medium text-sage-700 transition-colors flex items-center gap-2">
                  <Activity className="w-4 h-4" />
                  Live View
                </button>
              </div>

              <div className="relative h-96 bg-gradient-to-br from-sage-100 to-cream-100 rounded-2xl overflow-hidden border border-sage-200">
                {/* Placeholder for satellite/map */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <MapPin className="w-16 h-16 text-sage-400 mx-auto mb-4" />
                    <p className="text-sage-600 font-medium">Field Map Visualization</p>
                    <p className="text-sm text-sage-500 mt-1">Integrate satellite imagery API here</p>
                  </div>
                </div>

                {/* Field Markers */}
                <div className="absolute top-4 left-4 space-y-2">
                  {['North Field A', 'South Field B', 'East Field C'].map((field, i) => (
                    <div key={i} className="bg-white/90 backdrop-blur-sm rounded-xl px-3 py-2 shadow-lg border border-sage-200/50">
                      <p className="text-xs font-semibold text-sage-900">{field}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <div className={`w-2 h-2 rounded-full ${i === 0 ? 'bg-red-500' : 'bg-green-500'}`}></div>
                        <span className="text-xs text-sage-600">{i === 0 ? 'Needs attention' : 'Optimal'}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Weather Card */}
            <div className="bg-gradient-to-br from-blue-500 to-cyan-600 rounded-2xl p-6 text-white shadow-depth">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <p className="text-blue-100 text-sm mb-1">Today's Weather</p>
                  <p className="text-3xl font-bold">{weatherData.temp}</p>
                </div>
                <CloudRain className="w-12 h-12 text-blue-200" />
              </div>

              <p className="text-lg font-medium mb-6">{weatherData.condition}</p>

              <div className="space-y-3">
                <div className="flex items-center justify-between bg-white/10 backdrop-blur-sm rounded-xl p-3">
                  <div className="flex items-center gap-2">
                    <Thermometer className="w-4 h-4" />
                    <span className="text-sm">Humidity</span>
                  </div>
                  <span className="font-semibold">{weatherData.humidity}</span>
                </div>

                <div className="flex items-center justify-between bg-white/10 backdrop-blur-sm rounded-xl p-3">
                  <div className="flex items-center gap-2">
                    <Wind className="w-4 h-4" />
                    <span className="text-sm">Wind Speed</span>
                  </div>
                  <span className="font-semibold">{weatherData.wind}</span>
                </div>

                <div className="flex items-center justify-between bg-white/10 backdrop-blur-sm rounded-xl p-3">
                  <div className="flex items-center gap-2">
                    <CloudRain className="w-4 h-4" />
                    <span className="text-sm">Rain Chance</span>
                  </div>
                  <span className="font-semibold">{weatherData.precipitation}</span>
                </div>
              </div>

              <button className="w-full mt-4 bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-xl py-3 font-medium transition-colors">
                7-Day Forecast
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Smart Irrigation Recommendations */}
            <div className="bg-white/70 backdrop-blur-md rounded-2xl p-6 border border-sage-200/50 shadow-soft">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h3 className="text-xl font-bold text-sage-900">Smart Recommendations</h3>
                  <p className="text-sm text-sage-600">AI-powered farming insights</p>
                </div>
                <Zap className="w-6 h-6 text-amber-500" />
              </div>

              <div className="space-y-4">
                {recommendations.map((rec) => (
                  <div
                    key={rec.id}
                    className="group bg-gradient-to-r from-cream-50 to-white rounded-2xl p-4 border border-sage-200/50 hover:shadow-lg hover:border-primary-300 transition-all cursor-pointer"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-sage-900 group-hover:text-primary-700 transition-colors">
                        {rec.title}
                      </h4>
                      <span
                        className={`text-xs px-2 py-1 rounded-lg font-medium ${
                          rec.priority === 'high'
                            ? 'bg-red-100 text-red-700'
                            : 'bg-amber-100 text-amber-700'
                        }`}
                      >
                        {rec.priority}
                      </span>
                    </div>
                    <p className="text-sm text-sage-600 mb-3">{rec.description}</p>
                    <div className="flex items-center gap-2 text-xs text-sage-500">
                      <Calendar className="w-3 h-3" />
                      <span>{rec.time}</span>
                    </div>
                  </div>
                ))}
              </div>

              <button className="w-full mt-4 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-xl py-3 font-medium hover:shadow-lg transition-shadow">
                View All Recommendations
              </button>
            </div>

            {/* Recent Alerts */}
            <div className="bg-white/70 backdrop-blur-md rounded-2xl p-6 border border-sage-200/50 shadow-soft">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h3 className="text-xl font-bold text-sage-900">Recent Alerts</h3>
                  <p className="text-sm text-sage-600">Field status updates</p>
                </div>
                <AlertCircle className="w-6 h-6 text-amber-500" />
              </div>

              <div className="space-y-4">
                {alerts.map((alert) => (
                  <div
                    key={alert.id}
                    className={`bg-gradient-to-r rounded-2xl p-4 border transition-all ${
                      alert.type === 'warning'
                        ? 'from-amber-50 to-orange-50 border-amber-200'
                        : alert.type === 'success'
                        ? 'from-green-50 to-emerald-50 border-green-200'
                        : 'from-blue-50 to-cyan-50 border-blue-200'
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <div
                        className={`w-2 h-2 rounded-full mt-2 ${
                          alert.urgent ? 'bg-red-500 animate-pulse' : 'bg-sage-400'
                        }`}
                      ></div>
                      <div className="flex-1">
                        <h4 className="font-semibold text-sage-900 mb-1">{alert.title}</h4>
                        <p className="text-sm text-sage-700 mb-2">{alert.field}</p>
                        <p className="text-xs text-sage-500">{alert.time}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <button className="w-full mt-4 bg-sage-100 hover:bg-sage-200 text-sage-700 rounded-xl py-3 font-medium transition-colors">
                View All Alerts
              </button>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-gradient-to-br from-primary-500 to-emerald-600 rounded-2xl p-8 text-white shadow-depth">
            <h3 className="text-2xl font-bold mb-2">Ready to optimize your farm?</h3>
            <p className="text-primary-100 mb-6">Take quick actions to improve efficiency</p>
            
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <button className="bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-xl p-4 text-left transition-all hover:scale-105">
                <Droplets className="w-8 h-8 mb-2" />
                <p className="font-semibold">Schedule Irrigation</p>
                <p className="text-sm text-primary-100 mt-1">Set up automatic watering</p>
              </button>
              
              <button className="bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-xl p-4 text-left transition-all hover:scale-105">
                <BarChart3 className="w-8 h-8 mb-2" />
                <p className="font-semibold">View Analytics</p>
                <p className="text-sm text-primary-100 mt-1">Detailed performance reports</p>
              </button>
              
              <button className="bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-xl p-4 text-left transition-all hover:scale-105">
                <Settings className="w-8 h-8 mb-2" />
                <p className="font-semibold">Configure Sensors</p>
                <p className="text-sm text-primary-100 mt-1">Manage IoT devices</p>
              </button>
            </div>
          </div>
        </main>
      </div>

      {/* Floating Chat Assistant */}
      <AssistantBubble />
    </div>
  );
};

export default Dashboard;
