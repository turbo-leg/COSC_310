import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../lib/api';
import { Map, Clock, ArrowLeft, Package, CheckCircle, Truck, Utensils } from 'lucide-react';

export default function OrderTracker() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [tracker, setTracker] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchTracker = async () => {
      try {
        const res = await api.get(`/orders/${id}/track`);
        setTracker(res.data);
      } catch (err) {
        setError('Failed to load tracking info for Order #' + id);
      }
    };
    fetchTracker();
    const interval = setInterval(fetchTracker, 15000); // Poll every 15s
    return () => clearInterval(interval);
  }, [id]);

  if (error) return <div className="p-8 text-red-500 text-center font-bold mt-20">{error}</div>;
  if (!tracker) return <div className="p-8 text-center text-gray-500 font-bold animate-pulse mt-20">Locating Order Route...</div>;

  const phases = ['pending', 'accepted', 'preparing', 'assigned', 'out-for-delivery', 'delivered'];
  const currentIndex = phases.indexOf(tracker.status.toLowerCase());

  return (
    <div className="max-w-3xl mx-auto p-6 md:p-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <button onClick={() => navigate('/orders')} className="flex items-center text-gray-500 hover:text-blue-600 mb-8 transition-colors font-medium">
        <ArrowLeft className="w-5 h-5 mr-2" /> Back to My Orders
      </button>

      <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
         <div className="bg-gray-900 text-white p-8 border-b border-gray-800">
           <h1 className="text-3xl font-black mb-2 flex items-center gap-3">
             <Map className="w-8 h-8 text-blue-400" /> Tracking Order #{tracker.orderId}
           </h1>
           <div className="flex flex-wrap items-center gap-4 text-gray-300 font-medium">
             <span className="flex items-center gap-1"><Clock className="w-5 h-5 text-gray-400"/> ETA: {tracker.estimatedArrivalTime}</span>
             <span className="bg-blue-600/20 text-blue-400 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">{tracker.minutesRemaining} mins left</span>
           </div>
         </div>

         <div className="p-8">
           <h3 className="text-xl font-bold text-gray-900 mb-8 border-b pb-4">Live Route Progress</h3>
           
           <div className="relative">
             <div className="absolute left-8 top-0 bottom-0 w-1 bg-gray-100 rounded-full" />
             
             <div className="space-y-10 relative z-10">
               {[
                 { key: 'pending', label: 'Order Received', icon: <Package />, color: 'bg-yellow-500' },
                 { key: 'accepted', label: 'Restaurant Accepted', icon: <Utensils />, color: 'bg-blue-500' },
                 { key: 'preparing', label: 'Cooking Your Meal', icon: <Utensils />, color: 'bg-purple-500' },
                 { key: 'assigned', label: 'Driver Assigned', icon: <Truck />, color: 'bg-orange-500' },
                 { key: 'out-for-delivery', label: 'Out for Delivery', icon: <Truck />, color: 'bg-indigo-500' },
                 { key: 'delivered', label: 'Delivered', icon: <CheckCircle />, color: 'bg-green-500' }
               ].map((phase, idx) => {
                 const isCompleted = idx <= currentIndex;
                 const isActive = idx === currentIndex;
                 
                 return (
                   <div key={phase.key} className="flex items-center gap-6 group">
                     <div className={`w-16 h-16 shrink-0 rounded-full flex items-center justify-center text-white shadow-sm border-4 border-white transition-all duration-500 ${isActive ? 'scale-110 shadow-md ring-4 ring-gray-50' : ''} ${isCompleted ? phase.color : 'bg-gray-200 group-hover:bg-gray-300'}`}>
                       {React.cloneElement(phase.icon, { className: 'w-6 h-6' })}
                     </div>
                     <div>
                       <h4 className={`text-lg font-bold ${isActive ? 'text-gray-900' : isCompleted ? 'text-gray-600' : 'text-gray-400'}`}>
                         {phase.label}
                       </h4>
                       {isActive && <div className="text-sm text-blue-600 font-bold bg-blue-50 px-2 py-0.5 rounded-md inline-block mt-1">Current Status</div>}
                     </div>
                   </div>
                 );
               })}
             </div>
           </div>
         </div>
      </div>
    </div>
  );
}
