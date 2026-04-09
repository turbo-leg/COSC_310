import {
  Activity,
  AlertCircle,
  CheckCircle,
  Receipt,
  RotateCcw,
  Store,
  Users,
  XCircle,
} from 'lucide-react';
import { useEffect, useState } from 'react';
import AdminUserManagement from '../components/AdminUserManagement';
import api from '../lib/api';

const REASON_LABELS = {
  never_arrived: 'Order never arrived',
  wrong_order: 'Wrong order received',
  poor_quality: 'Poor food quality',
  missing_items: 'Items missing from order',
  other: 'Other',
};

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [refunds, setRefunds] = useState([]);
  const [refundsLoading, setRefundsLoading] = useState(true);
  const [refundsError, setRefundsError] = useState('');

  const token = localStorage.getItem('token');
  const decodedToken = token ? JSON.parse(atob(token.split('.')[1])) : null;
  const userId = decodedToken?.userId;

  const [promoCode, setPromoCode] = useState('');
  const [discount, setDiscount] = useState(0);
  const [expiry, setExpiry] = useState('');
  const [promoSuccess, setPromoSuccess] = useState(false);
  const [promoError, setPromoError] = useState('');

  const handleCreatePromo = async () => {
    if (!promoCode || !discount || !expiry) {
      setPromoError('Please fill all fields including expiry date');
      setPromoSuccess(false);
      return;
    }

    const token = localStorage.getItem('token');
    const decodedToken = token ? JSON.parse(atob(token.split('.')[1])) : null;
    const userId = decodedToken?.userId;

    try {
      const payload = {
        code: promoCode.toUpperCase(),
        discount: Number(discount),
        expiry: new Date(`${expiry}T00:00:00Z`).toISOString(),
        assigned_users: [],
      };

      await api.post(`/admin/promo?user_id=${userId}`, payload);

      setPromoSuccess(true);
      setPromoError('');
      setPromoCode('');
      setDiscount(0);
      setExpiry('');
    } catch (err) {
      console.error(err.response?.data);
      setPromoError(
        err.response?.data?.detail || JSON.stringify(err.response?.data) || 'Failed to create promo'
      );
      setPromoSuccess(false);
    }
  };

  const fetchStats = async () => {
    const token = localStorage.getItem('token');
    const decodedToken = token ? JSON.parse(atob(token.split('.')[1])) : null;
    const userId = decodedToken?.userId;

    try {
      setLoading(true);
      const res = await api.get(`/admin/stats?user_id=${userId}`);
      setStats(res.data);
    } catch (err) {
      setError('Failed to fetch admin stats. Ensure you have admin privileges.');
    } finally {
      setLoading(false);
    }
  };

  const fetchRefunds = async () => {
    const token = localStorage.getItem('token');
    const decodedToken = token ? JSON.parse(atob(token.split('.')[1])) : null;
    const userId = decodedToken?.userId;

    try {
      setRefundsLoading(true);
      setRefundsError('');
      const res = await api.get(`/refunds?user_id=${userId}`);
      setRefunds(res.data);
    } catch (err) {
      setRefundsError('Failed to load refund requests.');
    } finally {
      setRefundsLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
    fetchRefunds();
  }, []);

  const handleRefundDecision = async (refundId, status) => {
    const token = localStorage.getItem('token');
    const decodedToken = token ? JSON.parse(atob(token.split('.')[1])) : null;
    const userId = decodedToken?.userId;

    try {
      await api.patch(`/refunds/${refundId}?user_id=${userId}`, { status });
      fetchRefunds();
    } catch (err) {
      alert('Failed to update refund status.');
    }
  };

  const getRefundStatusStyle = (status) => {
    if (status === 'approved') return 'bg-green-100 text-green-700 border-green-200';
    if (status === 'denied') return 'bg-red-100 text-red-700 border-red-200';
    return 'bg-yellow-100 text-yellow-700 border-yellow-200';
  };

  const StatCard = ({ title, value, icon, colorClass }) => (
    <div className="bg-card text-card-foreground/80 backdrop-blur-xl border border-border/50 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 transform hover:-translate-y-1">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-muted-foreground mb-1">{title}</p>
          <h3 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600">{value}</h3>
        </div>
        <div className={`p-4 rounded-xl ${colorClass}`}>
          {icon}
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-muted text-muted-foreground/50 p-8 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-extrabold tracking-tight text-foreground">Admin Dashboard</h1>
          <p className="text-muted-foreground mt-2">Manage the platform and view system statistics.</p>
        </div>
        <button
          onClick={fetchStats}
          className="px-4 py-2 bg-card text-card-foreground border border-border rounded-lg hover:bg-muted transition-colors shadow-sm font-medium"
        >
          Refresh Stats
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="flex items-center gap-3 p-4 bg-red-50 text-red-700 rounded-xl border border-red-100">
          <AlertCircle className="w-5 h-5 text-red-500" />
          <p className="font-medium">{error}</p>
        </div>
      )}

      {/* Stats */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-pulse">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-32 bg-accent text-accent-foreground rounded-2xl"></div>
          ))}
        </div>
      ) : stats ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard title="Total Users" value={stats.total_users || 0} icon={<Users className="w-6 h-6 text-blue-600" />} colorClass="bg-secondary/20" />
          <StatCard title="Total Restaurants" value={stats.total_restaurants || 0} icon={<Store className="w-6 h-6 text-purple-600" />} colorClass="bg-purple-100" />
          <StatCard title="Total Orders" value={stats.total_orders || 0} icon={<Receipt className="w-6 h-6 text-green-600" />} colorClass="bg-green-100" />
          <StatCard title="System Active" value="100%" icon={<Activity className="w-6 h-6 text-orange-600" />} colorClass="bg-accent/20" />
        </div>
      ) : null}

      {/* Promo Code Section */}
      <div className="mt-12 bg-card text-card-foreground rounded-3xl shadow-sm border border-border/60 overflow-hidden">
        <div className="border-b border-border bg-muted text-muted-foreground/50 p-6">
          <h2 className="text-xl font-bold text-foreground">Create Promo Code</h2>
          <p className="text-sm text-muted-foreground mt-1">Set discount codes for users</p>
        </div>
        <div className="p-6 space-y-4">
          <input
            type="text"
            placeholder="Promo Code"
            className="w-full px-4 py-2 border border-border rounded-lg"
            value={promoCode}
            onChange={(e) => setPromoCode(e.target.value)}
          />
          <input
            type="number"
            placeholder="Discount (%)"
            className="w-full px-4 py-2 border border-border rounded-lg"
            value={discount}
            onChange={(e) => setDiscount(Number(e.target.value))}
          />
          <input
            type="date"
            className="w-full px-4 py-2 border border-border rounded-lg"
            value={expiry}
            onChange={(e) => setExpiry(e.target.value)}
          />
          <button
            onClick={handleCreatePromo}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Create Promo
          </button>
          {promoSuccess && <p className="text-green-600">Promo created!</p>}
          {promoError && <p className="text-red-600">{promoError}</p>}
        </div>
      </div>

      <div className="bg-card text-card-foreground rounded-3xl shadow-sm border border-border/60 overflow-hidden">
        <div className="border-b border-border bg-muted/50 p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <RotateCcw className="w-5 h-5 text-amber-500" />
            <div>
              <h2 className="text-xl font-bold text-foreground">Refund Requests</h2>
              <p className="text-sm text-muted-foreground mt-0.5">Review and resolve customer refund requests.</p>
            </div>
          </div>
          <button type="button" onClick={fetchRefunds} className="text-sm font-bold text-blue-600 hover:text-blue-800 transition-colors">Refresh</button>
        </div>
        <div className="p-6">
          {refundsError && (
            <div className="flex items-center gap-3 p-4 bg-red-50 text-red-700 rounded-xl border border-red-100 mb-4">
              <AlertCircle className="w-5 h-5 text-red-500" />
              <p className="font-medium">{refundsError}</p>
            </div>
          )}
          {refundsLoading ? (
            <div className="space-y-3 animate-pulse">
              {[1, 2, 3].map(i => <div key={i} className="h-20 bg-muted rounded-xl"></div>)}
            </div>
          ) : refunds.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground font-medium">No refund requests yet.</div>
          ) : (
            <div className="space-y-4">
              {refunds.map(refund => (
                <div key={refund.refundId} className="border border-border rounded-2xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:shadow-sm transition">
                  <div className="space-y-1">
                    <div className="flex items-center gap-3 flex-wrap">
                      <span className="font-bold text-foreground">Refund #{refund.refundId}</span>
                      <span className="text-sm text-muted-foreground">&mdash; Order #{refund.orderId}</span>
                      <span className={`px-3 py-0.5 rounded-full text-xs font-bold uppercase border ${getRefundStatusStyle(refund.status)}`}>
                        {refund.status}
                      </span>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      <span className="font-semibold text-foreground">Reason:</span> {REASON_LABELS[refund.reason] || refund.reason}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      <span className="font-semibold text-foreground">Description:</span> {refund.description}
                    </p>
                    <p className="text-xs text-muted-foreground/80">
                      Submitted: {new Date(refund.createdAt).toLocaleString()} &bull; User ID: {refund.userId}
                    </p>
                  </div>
                  {refund.status === 'pending' && (
                    <div className="flex gap-3 shrink-0">
                      <button
                        type="button"
                        onClick={() => handleRefundDecision(refund.refundId, 'approved')}
                        className="flex items-center gap-2 px-5 py-2.5 bg-green-500 text-white rounded-xl font-semibold hover:bg-green-600 transition text-sm"
                      >
                        <CheckCircle className="w-4 h-4" /> Approve
                      </button>
                      <button
                        type="button"
                        onClick={() => handleRefundDecision(refund.refundId, 'denied')}
                        className="flex items-center gap-2 px-5 py-2.5 bg-red-50 text-red-600 rounded-xl font-semibold hover:bg-red-100 transition border border-red-200 text-sm"
                      >
                        <XCircle className="w-4 h-4" /> Deny
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="mt-12 bg-card text-card-foreground rounded-3xl shadow-sm border border-border/60 overflow-hidden">
        <div className="border-b border-border bg-muted/50 p-6">
          <h2 className="text-xl font-bold text-foreground">User Management</h2>
          <p className="text-sm text-muted-foreground mt-1">Review and manage registered users.</p>
        </div>
        <div className="p-6">
          <AdminUserManagement />
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;