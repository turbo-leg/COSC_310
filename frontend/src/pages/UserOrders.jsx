import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../lib/api';
import { Package, Clock, XCircle, ArrowRight } from 'lucide-react';

export default function UserOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  // Using user 4 as fallback mapping
  const userId = localStorage.getItem('userId') || 4;

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const res = await api.get(`/orders/users/${userId}/orders`);
      setOrders(res.data.reverse());
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (orderId) => {
    if (!window.confirm("Are you sure you want to cancel this order?")) return;
    try {
      await api.put(`/orders/${orderId}/cancel`);
      fetchOrders();
    } catch (err) {
      alert("Cannot cancel order once preparation has started.");
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'pending': return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      case 'accepted': return 'bg-blue-100 text-blue-700 border-blue-200';
      case 'preparing': return 'bg-purple-100 text-purple-700 border-purple-200';
      case 'assigned': case 'out-for-delivery': return 'bg-orange-100 text-orange-700 border-orange-200';
      case 'delivered': return 'bg-green-100 text-green-700 border-green-200';
      case 'cancelled': return 'bg-red-100 text-red-700 border-red-200';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6 md:p-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center gap-4 mb-10">
        <div className="p-4 bg-blue-100 text-blue-600 rounded-2xl">
          <Package className="w-8 h-8" />
        </div>
        <div>
          <h1 className="text-4xl font-extrabold text-gray-900">My Orders</h1>
          <p className="text-gray-500">Track and manage your recent meal requests.</p>
        </div>
      </div>

      {loading ? (
        <div className="space-y-4 animate-pulse">
          {[1, 2, 3].map(i => <div key={i} className="h-32 bg-gray-100 rounded-2xl"></div>)}
        </div>
      ) : orders.length === 0 ? (
        <div className="text-center py-20 bg-white rounded-3xl border border-gray-100 shadow-sm">
          <Package className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-2xl font-bold text-gray-900">No orders yet</h3>
          <p className="text-gray-500 mt-2">Looks like you haven't ordered anything.</p>
          <button onClick={() => navigate('/')} className="mt-6 bg-blue-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-blue-700 transition shadow-md">Browse Restaurants</button>
        </div>
      ) : (
        <div className="grid gap-6">
          {orders.map(order => (
            <div key={order.orderId} className="bg-white rounded-3xl shadow-sm border border-gray-100 p-6 flex flex-col md:flex-row gap-6 items-center hover:shadow-md transition">
              <div className="flex-1 space-y-4 w-full">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 border-b pb-2 mb-2">Order #{order.orderId}</h3>
                    <p className="text-sm font-medium text-gray-500 mt-1">
                      Placed on {new Date(order.createdAt).toLocaleString()}
                    </p>
                  </div>
                  <span className={`px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider border ${getStatusColor(order.status)}`}>
                    {order.status}
                  </span>
                </div>
                
                <div className="flex flex-wrap gap-4 text-sm bg-gray-50 p-4 rounded-xl">
                  <div className="flex items-center gap-2">
                    <span className="text-gray-500">Payment:</span>
                    <span className="font-bold underline decoration-wavy decoration-green-400 capitalize">{order.payment_status}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-gray-500">Total:</span>
                    <span className="font-bold text-gray-900">${order.order_value.toFixed(2)}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-gray-500">Items:</span>
                    <span className="font-bold text-gray-900">{order.items?.length || 0}</span>
                  </div>
                </div>
              </div>

              <div className="flex flex-row md:flex-col gap-3 w-full md:w-auto mt-4 md:mt-0 justify-center">
                <button 
                  onClick={() => navigate(`/order/${order.orderId}/track`)}
                  className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-gray-900 text-white rounded-xl font-medium hover:bg-black transition shadow-sm"
                >
                  <Clock className="w-4 h-4" /> Track
                </button>
                {order.status === 'pending' && (
                  <button 
                    onClick={() => handleCancel(order.orderId)}
                    className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-red-50 text-red-600 rounded-xl font-medium hover:bg-red-100 transition"
                  >
                    <XCircle className="w-4 h-4" /> Cancel
                  </button>
                )}
                {order.payment_status?.toLowerCase() === 'pending' && order.status !== 'cancelled' && (
                  <button 
                    onClick={() => navigate(`/payment/${order.orderId}`, { state: { amount: order.order_value } })}
                    className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-green-50 text-green-700 rounded-xl font-medium hover:bg-green-100 transition border border-green-200"
                  >
                    Make Payment <ArrowRight className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
