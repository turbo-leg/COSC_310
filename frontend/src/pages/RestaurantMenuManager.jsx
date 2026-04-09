import React, { useEffect, useState } from 'react';
import api from '../lib/api';
import { PlusCircle, Edit2, Trash2, Check, X, Utensils, AlertCircle } from 'lucide-react';

export default function RestaurantMenuManager() {
  const [menu, setMenu] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const token = localStorage.getItem('token');
  const decodedToken = token ? JSON.parse(atob(token.split('.')[1])) : null;
  const restaurantId = decodedToken?.restaurantId;

  const [newItem, setNewItem] = useState({ name: '', description: '', price: '' });
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({ name: '', description: '', price: '' });

  const fetchMenu = async () => {
    try {
      setLoading(true);
      if (!restaurantId) return;
      const res = await api.get(`/restaurant/${restaurantId}/menu`);
      setMenu(res.data);
    } catch (err) {
      setError('Failed to fetch menu');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMenu();
  }, [restaurantId]);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.post(`/restaurant/${restaurantId}/menu`, {
        name: newItem.name,
        description: newItem.description,
        price: parseFloat(newItem.price)
      });
      setNewItem({ name: '', description: '', price: '' });
      fetchMenu();
    } catch (err) {
      alert("Failed to create menu item");
    }
  };

  const startEditing = (item) => {
    setEditingId(item.itemId);
    setEditForm({ name: item.name, description: item.description, price: item.price.toString() });
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await api.put(`/restaurant/${restaurantId}/menu/${editingId}`, {
        name: editForm.name,
        description: editForm.description,
        price: parseFloat(editForm.price)
      });
      setEditingId(null);
      fetchMenu();
    } catch (err) {
      alert("Failed to update item");
    }
  };

  const handleDelete = async (itemId) => {
    if (!window.confirm("Delete this menu item?")) return;
    try {
      await api.delete(`/restaurant/${restaurantId}/menu/${itemId}`);
      fetchMenu();
    } catch (err) {
      alert("Failed to delete item");
    }
  };

  if (!restaurantId) return <div className="p-8 text-center text-red-500 font-bold mt-20">Restaurant identity not found in token. Please log in as a restaurant owner.</div>;

  return (
    <div className="max-w-5xl mx-auto p-6 md:p-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center gap-4 mb-10">
        <div className="p-4 bg-accent/20 text-orange-600 rounded-2xl">
          <Utensils className="w-8 h-8" />
        </div>
        <div>
          <h1 className="text-4xl font-extrabold text-foreground">Menu Management</h1>
          <p className="text-muted-foreground mt-1">Add, edit, or delete items from your public restaurant menu.</p>
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-3 p-4 mb-8 bg-red-50 text-red-700 rounded-xl border border-red-100">
          <AlertCircle className="w-5 h-5" /> <p className="font-bold">{error}</p>
        </div>
      )}

      {/* Add New Item Form */}
      <div className="bg-card text-card-foreground p-8 rounded-3xl shadow-sm border border-border mb-8 relative overflow-hidden">
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-orange-400 to-orange-600" />
        <h2 className="text-xl font-bold mb-6 text-foreground">Create New Item</h2>
        <form onSubmit={handleCreate} className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <input required type="text" placeholder="Item Name" value={newItem.name} onChange={e => setNewItem({...newItem, name: e.target.value})} className="px-4 py-3 bg-muted text-muted-foreground border border-border rounded-xl focus:ring-2 focus:ring-primary-500 outline-none transition-all font-medium" />
          <input required type="text" placeholder="Description" value={newItem.description} onChange={e => setNewItem({...newItem, description: e.target.value})} className="px-4 py-3 bg-muted text-muted-foreground border border-border rounded-xl focus:ring-2 focus:ring-primary-500 outline-none transition-all font-medium" />
          <input required type="number" step="0.01" min="0" placeholder="Price ($)" value={newItem.price} onChange={e => setNewItem({...newItem, price: e.target.value})} className="px-4 py-3 bg-muted text-muted-foreground border border-border rounded-xl focus:ring-2 focus:ring-primary-500 outline-none transition-all font-medium" />
          <button type="submit" className="bg-primary text-primary-foreground text-primary-foreground font-bold py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-primary/90 transition-colors shadow-sm">
            <PlusCircle className="w-5 h-5" /> Add Item
          </button>
        </form>
      </div>

      {/* Menu List */}
      <div className="bg-card text-card-foreground rounded-3xl shadow-sm border border-border overflow-hidden">
        <div className="px-8 py-5 border-b border-border bg-muted text-muted-foreground/50">
          <h2 className="text-lg font-bold text-foreground">Active Menu Items</h2>
        </div>
        <div className="divide-y divide-gray-100">
          {loading ? (
             <div className="p-12 text-center text-muted-foreground font-bold animate-pulse">Loading active menu catalogue...</div>
          ) : menu.length === 0 ? (
             <div className="p-16 text-center bg-muted text-muted-foreground/30">
               <Utensils className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
               <h3 className="text-foreground font-bold text-xl">Your menu is empty</h3>
               <p className="text-muted-foreground mt-2 font-medium">Start adding items using the form above!</p>
             </div>
          ) : menu.map(item => (
            <div key={item.itemId} className="p-6 md:px-8 flex flex-col md:flex-row gap-4 items-center hover:bg-muted text-muted-foreground transition-colors">
              {editingId === item.itemId ? (
                <form onSubmit={handleUpdate} className="flex-1 flex flex-col md:flex-row gap-4 w-full">
                  <input required type="text" value={editForm.name} onChange={e => setEditForm({...editForm, name: e.target.value})} className="flex-1 px-4 py-2.5 bg-card text-card-foreground border border-border rounded-xl outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 font-medium" />
                  <input required type="text" value={editForm.description} onChange={e => setEditForm({...editForm, description: e.target.value})} className="flex-1 px-4 py-2.5 bg-card text-card-foreground border border-border rounded-xl outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 font-medium" />
                  <input required type="number" step="0.01" min="0" value={editForm.price} onChange={e => setEditForm({...editForm, price: e.target.value})} className="w-full md:w-32 px-4 py-2.5 bg-card text-card-foreground border border-border rounded-xl outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 font-bold" />
                  <div className="flex items-center gap-2 mt-2 md:mt-0 justify-end">
                    <button type="submit" className="px-4 py-2.5 bg-green-100 text-green-700 hover:bg-green-200 rounded-xl transition-colors font-bold flex items-center gap-2"><Check className="w-5 h-5"/> Save</button>
                    <button type="button" onClick={() => setEditingId(null)} className="px-4 py-2.5 bg-accent text-accent-foreground text-muted-foreground hover:bg-accent/80 text-accent-foreground rounded-xl transition-colors font-bold flex items-center gap-2"><X className="w-5 h-5"/> Cancel</button>
                  </div>
                </form>
              ) : (
                <>
                  <div className="flex-1 w-full text-left">
                    <h3 className="text-lg font-bold text-foreground">{item.name}</h3>
                    <p className="text-muted-foreground text-sm mt-1">{item.description}</p>
                  </div>
                  <div className="font-black text-green-600 text-xl w-32 md:text-right shrink-0">${item.price.toFixed(2)}</div>
                  <div className="flex gap-2 w-full md:w-auto shrink-0 justify-end mt-4 md:mt-0">
                    <button onClick={() => startEditing(item)} className="px-4 py-2.5 text-blue-600 bg-secondary/10 flex items-center gap-2 font-bold hover:bg-secondary/20 rounded-xl transition-colors"><Edit2 className="w-4 h-4" /> Edit</button>
                    <button onClick={() => handleDelete(item.itemId)} className="px-4 py-2.5 text-red-600 flex items-center gap-2 font-bold bg-red-50 hover:bg-red-100 rounded-xl transition-colors"><Trash2 className="w-4 h-4" /> Delete</button>
                  </div>
                </>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
