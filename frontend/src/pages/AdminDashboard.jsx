import React, { useEffect, useState } from 'react';
import api from '../lib/api';
import AdminUserManagement from '../components/AdminUserManagement';
import { Activity, Users, Store, Receipt, AlertCircle } from 'lucide-react';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    try {
      setLoading(true);
      // Assuming admin userId is available in context/localstorage
      const userId = localStorage.getItem('userId') || 3; // fallback for testing (3 is Admin in users.csv)
      const res = await api.get(`/admin/stats?user_id=${userId}`);
      setStats(res.data);
    } catch (err) {
      setError('Failed to fetch admin stats. Ensure you have admin privileges.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const StatCard = ({ title, value, icon, colorClass }) => (
    <div className="bg-white/80 backdrop-blur-xl border border-gray-200/50 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 transform hover:-translate-y-1">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500 mb-1">{title}</p>
          <h3 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600">{value}</h3>
        </div>
        <div className={`p-4 rounded-xl ${colorClass}`}>
          {icon}
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50/50 p-8 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-extrabold tracking-tight text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-500 mt-2">Manage the platform and view system statistics.</p>
        </div>
        <button onClick={fetchStats} className="px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors shadow-sm font-medium">
          Refresh Stats
        </button>
      </div>

      {error && (
        <div className="flex items-center gap-3 p-4 bg-red-50 text-red-700 rounded-xl border border-red-100">
          <AlertCircle className="w-5 h-5 text-red-500" />
          <p className="font-medium">{error}</p>
        </div>
      )}

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-pulse">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-32 bg-gray-200 rounded-2xl"></div>
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
            title="Total Restaurants" 
            value={stats.total_restaurants || 0} 
            icon={<Store className="w-6 h-6 text-purple-600" />} 
            colorClass="bg-purple-100" 
          />
          <StatCard 
            title="Total Orders" 
            value={stats.total_orders || 0} 
            icon={<Receipt className="w-6 h-6 text-green-600" />} 
            colorClass="bg-green-100" 
          />
          <StatCard 
            title="System Active" 
            value="100%" 
            icon={<Activity className="w-6 h-6 text-orange-600" />} 
            colorClass="bg-orange-100" 
          />
        </div>
      ) : null}

      <div className="mt-12 bg-white rounded-3xl shadow-sm border border-gray-200/60 overflow-hidden">
        <div className="border-b border-gray-100 bg-gray-50/50 p-6">
          <h2 className="text-xl font-bold text-gray-900">User Management</h2>
          <p className="text-sm text-gray-500 mt-1">Review and manage registered users.</p>
        </div>
        <div className="p-6">
          <AdminUserManagement />
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
