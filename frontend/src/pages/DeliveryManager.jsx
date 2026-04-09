import React, { useState } from 'react';
import api from '../lib/api';
import { Truck, Navigation, CheckCircle } from 'lucide-react';

export default function DeliveryManager() {
  const [orderId, setOrderId] = useState('');
  const [deliveryId, setDeliveryId] = useState('');
  const [status, setStatus] = useState('');

  const handleAssign = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post(`/delivery/assign?order_id=${orderId}&delivery_id=${deliveryId}`);
      setStatus(`Success! Order #${res.data.order.orderId} assigned to driver #${deliveryId}.`);
    } catch (err) {
      alert("Failed to assign delivery. Verify order is ready.");
    }
  };

  return (
    <div className="max-w-xl mx-auto p-6 md:p-12 animate-in fade-in slide-in-from-bottom-4 duration-500 my-10">
      <div className="bg-card text-card-foreground p-8 rounded-3xl shadow-xl border border-border relative overflow-hidden">
        <div className="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-orange-400 to-orange-600" />
        
        <div className="flex items-center gap-4 mb-8 mt-2">
           <div className="p-4 bg-accent/10 text-orange-600 rounded-2xl">
             <Truck className="w-8 h-8" />
           </div>
           <div>
             <h2 className="text-3xl font-extrabold text-foreground">Dispatch Menu</h2>
             <p className="text-muted-foreground mt-1 font-medium">Assign a fleet driver to an active order</p>
           </div>
        </div>

        {status && (
          <div className="mb-6 p-4 bg-green-50 text-green-700 rounded-xl border border-green-200 flex items-center gap-3">
             <CheckCircle className="w-5 h-5 shrink-0" />
             <p className="font-bold">{status}</p>
          </div>
        )}

        <form onSubmit={handleAssign} className="space-y-6">
          <div>
            <label className="block text-sm font-bold text-muted-foreground mb-2">Order ID</label>
            <input 
              type="number"
              value={orderId}
              onChange={(e) => setOrderId(e.target.value)}
              placeholder="e.g. 5"
              required
              className="w-full px-5 py-4 rounded-xl border border-border bg-muted text-muted-foreground focus:bg-card text-card-foreground focus:ring-2 focus:ring-primary-500 transition-all font-mono outline-none"
            />
          </div>
          
          <div>
            <label className="block text-sm font-bold text-muted-foreground mb-2">Driver ID</label>
            <input 
              type="number"
              value={deliveryId}
              onChange={(e) => setDeliveryId(e.target.value)}
              placeholder="e.g. 12"
              required
              className="w-full px-5 py-4 rounded-xl border border-border bg-muted text-muted-foreground focus:bg-card text-card-foreground focus:ring-2 focus:ring-primary-500 transition-all font-mono outline-none"
            />
          </div>

          <button 
            type="submit" 
            className="w-full py-4 px-6 bg-primary text-primary-foreground text-primary-foreground rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-primary/90 transition-colors shadow-sm mt-4"
          >
            <Navigation className="w-5 h-5" /> Dispatch Driver
          </button>
        </form>
      </div>
    </div>
  );
}
