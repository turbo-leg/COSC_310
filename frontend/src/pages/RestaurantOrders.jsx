import React, { useEffect, useState } from 'react';
import api from '../lib/api';
import { Store, TrendingUp, CheckCircle, Clock } from 'lucide-react';

export default function RestaurantOrders() {
  const [orders, setOrders] = useState([]);
  const [revenue, setRevenue] = useState(0);
  const [loading, setLoading] = useState(true);
  
  const token = localStorage.getItem('token');
  let decodedToken = null;
  if (token) {
    try {
      decodedToken = JSON.parse(atob(token.split('.')[1]));
    } catch {
      decodedToken = null;
    }
  }
  // Backend treats missing restaurantId as userId for owners; path must be the venue id.
  const restaurantIdForOrders =
    decodedToken?.restaurantId != null && decodedToken.restaurantId !== ''
      ? Number(decodedToken.restaurantId)
      : decodedToken?.userId != null
        ? Number(decodedToken.userId)
        : null;
  // Revenue endpoint expects user_id = owner account id in the database.
  const ownerUserId =
    decodedToken?.userId != null ? Number(decodedToken.userId) : null;

  const fetchData = async () => {
    if (restaurantIdForOrders == null || Number.isNaN(restaurantIdForOrders)) {
      setOrders([]);
      setRevenue(0);
      setLoading(false);
      return;
    }
    try {
      setLoading(true);
      const ordersUrl = `/orders/restaurants/${restaurantIdForOrders}/orders`;
      const revUrl =
        ownerUserId != null && !Number.isNaN(ownerUserId)
          ? `/orders/restaurants/${restaurantIdForOrders}/revenue?user_id=${ownerUserId}`
          : null;
      const ordRes = await api.get(ordersUrl);
      setOrders(ordRes.data.reverse());
      if (revUrl) {
        const revRes = await api.get(revUrl);
        setRevenue(revRes.data.total_revenue || 0);
      } else {
        setRevenue(0);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [restaurantIdForOrders, ownerUserId]);

  const updateStatus = async (orderId, newStatus) => {
    try {
      await api.patch(`/orders/${orderId}/status`, { new_status: newStatus });
      fetchData();
    } catch (err) {
      alert("Failed to update status");
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6 md:p-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-6">
        <div className="flex items-center gap-4">
          <div className="p-4 bg-accent/20 text-orange-600 rounded-2xl border border-accent/20/50 shadow-sm">
            <Store className="w-8 h-8" />
          </div>
          <div>
            <h1 className="text-4xl font-extrabold text-foreground leading-tight">Restaurant Dashboard</h1>
            <p className="text-muted-foreground mt-1">Manage incoming orders and track your active earnings.</p>
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200/60 p-6 rounded-3xl flex items-center gap-6 shadow-sm min-w-[250px] transition-transform hover:-translate-y-1 duration-300">
          <div className="p-3 bg-card text-card-foreground/60 rounded-xl backdrop-blur-sm shadow-sm">
             <TrendingUp className="w-8 h-8 text-green-600" />
          </div>
          <div>
            <p className="text-sm font-bold text-green-800/60 uppercase tracking-widest mb-1">Revenue</p>
            <h2 className="text-4xl font-black text-green-700">${revenue.toFixed(2)}</h2>
          </div>
        </div>
      </div>

      <div className="bg-card text-card-foreground rounded-[2rem] shadow-sm border border-border overflow-hidden">
        <div className="px-8 py-6 border-b border-border bg-muted text-muted-foreground flex items-center justify-between">
          <h2 className="text-xl font-bold text-foreground flex items-center gap-3">
            <Clock className="w-5 h-5 text-blue-500" /> Active Order Queue
          </h2>
          <button onClick={fetchData} className="text-sm font-bold text-blue-600 hover:text-blue-800 transition-colors">Refresh</button>
        </div>
        
        <div className="p-8">
          {loading ? (
            <div className="text-center py-10 animate-pulse text-muted-foreground font-medium">Loading incoming orders...</div>
          ) : orders.length === 0 ? (
            <div className="text-center py-16 bg-muted text-muted-foreground/50 rounded-2xl border border-dashed border-border">
              <p className="text-muted-foreground text-lg font-medium">No orders have been placed yet.</p>
            </div>
          ) : (
            <div className="space-y-6">
              {orders.map(order => (
                <div key={order.orderId} className="bg-card text-card-foreground border border-border rounded-2xl p-6 hover:shadow-md hover:border-border transition-all duration-300">
                  <div className="flex flex-col lg:flex-row justify-between gap-6">
                    <div>
                       <div className="flex items-center gap-3 mb-2">
                         <h3 className="text-xl font-black text-foreground">Order #{order.orderId}</h3>
                         <span className="px-3 py-1 bg-muted text-muted-foreground font-bold uppercase tracking-wider text-xs rounded-lg">
                           {order.status}
                         </span>
                       </div>
                       <p className="text-sm text-muted-foreground font-medium">Customer ID: <span className="text-foreground">{order.userId}</span> • Payment: <span className={order.payment_status === 'pending' ? 'text-orange-500' : 'text-green-600'}>{order.payment_status}</span></p>
                       <p className="text-sm text-muted-foreground font-medium mt-1">Total Value: <span className="font-bold text-foreground">${order.order_value.toFixed(2)}</span></p>
                       <p className="text-xs text-muted-foreground mt-2 font-medium">Placed: {new Date(order.createdAt).toLocaleString()}</p>
                    </div>
                    
                    <div className="flex flex-wrap sm:flex-nowrap gap-3 items-center shrink-0">
                       {order.status === 'pending' && (
                         <button onClick={() => updateStatus(order.orderId, 'accepted')} className="w-full sm:w-auto px-6 py-3 bg-primary text-primary-foreground text-primary-foreground rounded-xl font-bold hover:bg-blue-700 shadow-sm transition">
                           Accept Order
                         </button>
                       )}
                       {order.status === 'accepted' && (
                         <button onClick={() => updateStatus(order.orderId, 'preparing')} className="w-full sm:w-auto px-6 py-3 bg-purple-600 text-primary-foreground rounded-xl font-bold hover:bg-purple-700 shadow-sm transition">
                           Start Preparing
                         </button>
                       )}
                       {order.status === 'preparing' && (
                         <button onClick={() => updateStatus(order.orderId, 'assigned')} className="w-full sm:w-auto px-6 py-3 bg-orange-600 text-primary-foreground rounded-xl font-bold hover:bg-orange-700 shadow-sm transition">
                           Pass to Delivery
                         </button>
                       )}
                       {order.status === 'assigned' && (
                         <button onClick={() => updateStatus(order.orderId, 'out-for-delivery')} className="w-full sm:w-auto px-6 py-3 bg-indigo-600 text-primary-foreground rounded-xl font-bold hover:bg-indigo-700 shadow-sm transition">
                           Out for Delivery
                         </button>
                       )}
                       {order.status === 'out-for-delivery' && (
                         <button onClick={() => updateStatus(order.orderId, 'delivered')} className="w-full sm:w-auto px-6 py-3 bg-green-600 text-primary-foreground rounded-xl font-bold hover:bg-green-700 shadow-sm transition flex items-center justify-center gap-2">
                           <CheckCircle className="w-5 h-5" /> Mark Delivered
                         </button>
                       )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
