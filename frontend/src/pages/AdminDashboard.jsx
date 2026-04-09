import React, { useEffect, useState } from 'react';
import api from '../lib/api';
import AdminUserManagement from '../components/AdminUserManagement';
import AdminMenuManagement from '../components/admin/AdminMenuManagement';
import { Activity, Users, Store, Receipt, AlertCircle, ShoppingBag, DollarSign } from 'lucide-react';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  // Filters
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [activeTab, setActiveTab] = useState('stats');

  const fetchStats = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const decodedToken = token ? JSON.parse(atob(token.split('.')[1])) : null;
      const userId = decodedToken?.userId;
      
      let params = `?user_id=${userId}`;
      if (startDate) params += `&start_date=${new Date(startDate).toISOString()}`;
      if (endDate) params += `&end_date=${new Date(endDate).toISOString()}`;
      if (statusFilter) params += `&status=${statusFilter}`;

      const res = await api.get(`/admin/stats${params}`);
      setStats(res.data);
    } catch (err) {
      setError('Failed to fetch admin stats. Ensure you have admin privileges.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, [startDate, endDate, statusFilter]);

  const StatCard = ({ title, value, icon, colorClass }) => (
    <div className="bg-card text-card-foreground/80 backdrop-blur-xl border border-border/50 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 transform hover:-translate-y-1">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-muted-foreground mb-1">{title}</p>
          <h3 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-400">{value}</h3>
        </div>
        <div className={`p-4 rounded-xl ${colorClass}`}>
          {icon}
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-muted text-muted-foreground/50 p-8 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-extrabold tracking-tight text-foreground">Admin Dashboard</h1>
          <p className="text-muted-foreground mt-2">Manage the platform and view system statistics.</p>
        </div>
        <button onClick={fetchStats} className="px-4 py-2 bg-card border border-border text-foreground rounded-lg hover:bg-muted transition-colors shadow-sm font-medium">
          Refresh Stats
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-4 border-b border-border pb-2">
        <button onClick={() => setActiveTab('stats')} className={`pb-2 px-1 font-semibold text-lg transition-colors ${activeTab === 'stats' ? 'text-primary border-b-2 border-primary' : 'text-muted-foreground hover:text-foreground'}`}>Statistics & Filters</button>
        <button onClick={() => setActiveTab('users')} className={`pb-2 px-1 font-semibold text-lg transition-colors ${activeTab === 'users' ? 'text-primary border-b-2 border-primary' : 'text-muted-foreground hover:text-foreground'}`}>User Management</button>
        <button onClick={() => setActiveTab('menu')} className={`pb-2 px-1 font-semibold text-lg transition-colors ${activeTab === 'menu' ? 'text-primary border-b-2 border-primary' : 'text-muted-foreground hover:text-foreground'}`}>Global Menu Stock</button>
      </div>

      {error && (
        <div className="flex items-center gap-3 p-4 bg-red-50 text-red-700 rounded-xl border border-red-100">
          <AlertCircle className="w-5 h-5 text-red-500" />
          <p className="font-medium">{error}</p>
        </div>
      )}

      {activeTab === 'stats' && (
      <>
        {/* Filters */}
        <div className="bg-card text-card-foreground border border-border rounded-xl p-4 flex flex-wrap gap-4 items-end shadow-sm">
          <div className="flex flex-col gap-1">
            <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Start Date</label>
            <input type="datetime-local" value={startDate} onChange={e => setStartDate(e.target.value)} className="border border-input bg-background text-foreground rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-ring focus:border-input" />
          </div>
          
          <div className="flex flex-col gap-1">
            <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">End Date</label>
            <input type="datetime-local" value={endDate} onChange={e => setEndDate(e.target.value)} className="border border-input bg-background text-foreground rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-ring focus:border-input" />
          </div>
          
          <div className="flex flex-col gap-1">
            <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Status</label>
            <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)} className="border border-input bg-background text-foreground rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-ring focus:border-input">
              <option value="">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="assigned">Assigned</option>
              <option value="picked_up">Picked Up</option>
              <option value="delivered">Delivered</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
          
          <button onClick={() => { setStartDate(''); setEndDate(''); setStatusFilter(''); }} className="px-4 py-2 text-sm bg-muted text-muted-foreground hover:bg-secondary rounded-lg transition-colors font-medium border border-border">
            Clear Filters
          </button>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-pulse">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-accent text-accent-foreground rounded-2xl"></div>
            ))}
          </div>
        ) : stats ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard 
              title="Total Users" 
              value={stats.total_users || 0} 
              icon={<Users className="w-6 h-6 text-blue-600" />} 
              colorClass="bg-blue-100" 
            />
            <StatCard 
              title="Total Menu Items" 
              value={stats.total_menu_items || 0} 
              icon={<ShoppingBag className="w-6 h-6 text-purple-600" />} 
              colorClass="bg-purple-100" 
            />
            <StatCard 
              title="Order Volume" 
              value={stats.total_orders || 0} 
              icon={<Receipt className="w-6 h-6 text-orange-600" />} 
              colorClass="bg-orange-100" 
            />
            <StatCard 
              title="Platform Revenue" 
              value={`$${(stats.total_revenue || 0).toFixed(2)}`} 
              icon={<DollarSign className="w-6 h-6 text-green-600" />} 
              colorClass="bg-green-100" 
            />
          </div>
        ) : null}
      </>
      )}

      {activeTab === 'users' && (
        <div className="bg-card text-card-foreground rounded-3xl shadow-sm border border-border/60 overflow-hidden">
          <div className="border-b border-border bg-muted text-muted-foreground/50 p-6">
            <h2 className="text-xl font-bold text-foreground">User Management</h2>
            <p className="text-sm text-muted-foreground mt-1">Review and manage registered users.</p>
          </div>
          <div className="p-6">
            <AdminUserManagement />
          </div>
        </div>
      )}

      {activeTab === 'menu' && (
        <div className="bg-card text-card-foreground rounded-3xl shadow-sm border border-border/60 overflow-hidden">
          <div className="border-b border-border bg-muted text-muted-foreground/50 p-6">
            <h2 className="text-xl font-bold text-foreground">Global Menu Stock Management</h2>
            <p className="text-sm text-muted-foreground mt-1">Actively toggle menu item availability across the entire platform.</p>
          </div>
          <div className="p-6">
            <AdminMenuManagement />
          </div>
        </div>
      )}

    </div>
  );
};

export default AdminDashboard;
