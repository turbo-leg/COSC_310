import React, { useState, useEffect } from 'react';
import api from '../../lib/api';
import { Shield, CheckCircle, XCircle } from 'lucide-react';

const AdminMenuManagement = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchMenu = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const decodedToken = token ? JSON.parse(atob(token.split('.')[1])) : null;
      const userId = decodedToken?.userId;
      
      const res = await api.get(`/admin/menu?user_id=${userId}`);
      setItems(res.data);
    } catch (err) {
      setError('Failed to fetch menu items.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMenu();
  }, []);

  const handleToggle = async (itemId, currentStatus) => {
    try {
      const token = localStorage.getItem('token');
      const decodedToken = token ? JSON.parse(atob(token.split('.')[1])) : null;
      const userId = decodedToken?.userId;
      
      await api.put(`/admin/menu/${itemId}/toggle-stock?user_id=${userId}`, { isActive: !currentStatus });
      fetchMenu();
    } catch {
      setError('Failed to toggle stock status.');
    }
  };

  if (loading) return <div className="animate-pulse flex space-x-4"><div className="flex-1 space-y-4 py-1"><div className="h-4 bg-muted rounded w-3/4"></div><div className="space-y-2"><div className="h-4 bg-muted rounded"></div></div></div></div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {items.map(item => (
          <div key={item.itemId} className="flex p-4 items-center justify-between border rounded-2xl bg-card transition hover:shadow-md">
            <div>
              <p className="font-bold text-foreground">{item.name}</p>
              <p className="text-sm text-muted-foreground w-40 truncate">{item.description}</p>
              <p className="text-sm font-semibold mt-1">${item.price.toFixed(2)}</p>
            </div>
            <div className="flex flex-col items-center justify-center gap-2">
              <span className={`text-xs font-bold px-2 py-1 rounded-full ${item.isActive ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
                {item.isActive ? 'In Stock' : 'Out of Stock'}
              </span>
              <button
                onClick={() => handleToggle(item.itemId, item.isActive)}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold ${
                  item.isActive 
                    ? "bg-red-50 hover:bg-red-100 text-red-600 border border-red-200" 
                    : "bg-green-50 hover:bg-green-100 text-green-600 border border-green-200"
                } transition-colors`}
              >
                {item.isActive ? <XCircle className="w-3 h-3" /> : <CheckCircle className="w-3 h-3" />}
                {item.isActive ? 'Deactivate' : 'Activate'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminMenuManagement;
