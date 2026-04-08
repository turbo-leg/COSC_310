import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../lib/api';
import { ShoppingBag, ArrowLeft, Plus, Minus, CreditCard, Loader2 } from 'lucide-react';

export default function OrderCheckout() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [restaurant, setRestaurant] = useState(null);
  const [menu, setMenu] = useState([]);
  const [cart, setCart] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [restRes, menuRes] = await Promise.all([
          api.get('/restaurants'),
          api.get(`/restaurant/${id}/menu`)
        ]);
        const r = restRes.data.find(x => x.userId === parseInt(id));
        setRestaurant(r);
        setMenu(menuRes.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  const updateCart = (itemId, delta) => {
    setCart(prev => {
      const q = (prev[itemId] || 0) + delta;
      if (q <= 0) {
        const c = { ...prev };
        delete c[itemId];
        return c;
      }
      return { ...prev, [itemId]: q };
    });
  };

  const getSubtotal = () => {
    return Object.entries(cart).reduce((sum, [itemId, qty]) => {
      const item = menu.find(m => m.itemId === parseInt(itemId));
      return sum + (item ? item.price * qty : 0);
    }, 0);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Loader2 className="w-12 h-12 text-blue-500 animate-spin" />
      </div>
    );
  }

  if (!restaurant) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-6">
        <h2 className="text-2xl font-bold mb-4">Restaurant Not Found</h2>
        <button onClick={() => navigate('/')} className="bg-blue-600 text-white px-6 py-2 rounded-full">
          Back to Home
        </button>
      </div>
    );
  }

  const handleCheckout = async () => {
    const itemsList = [];
    Object.entries(cart).forEach(([itemId, qty]) => {
      for (let i = 0; i < qty; i++) itemsList.push(parseInt(itemId));
    });

    try {
      const payload = {
        user_id: 4, // hardcoded test user for now until PR 5 Auth is built
        restaurant_id: parseInt(id),
        items: itemsList,
        distance_km: 3.5,
        time_minutes: 25
      };

      const res = await api.post('/orders/', payload);
      setCart({});
      navigate(`/payment/${res.data.orderId}`, { state: { amount: getSubtotal() } });
    } catch (err) {
      console.error("Order failed", err);
      alert("Failed to submit order.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-10 px-4 md:px-12 animate-in fade-in duration-500">
      <div className="max-w-5xl mx-auto">
        <button 
          onClick={() => navigate('/')}
          className="flex items-center text-gray-500 hover:text-blue-600 mb-8 transition-colors font-medium"
        >
          <ArrowLeft className="w-5 h-5 mr-2" /> Back to Restaurants
        </button>

        <div className="bg-white rounded-[2rem] shadow-sm border border-gray-100 overflow-hidden flex flex-col md:flex-row">
          
          {/* Menu Section */}
          <div className="md:w-2/3 p-8 border-r border-gray-100">
            <h1 className="text-4xl font-extrabold text-gray-900 mb-8">{restaurant.name}</h1>
            
            <h3 className="text-xl font-bold mb-6 text-gray-800 flex items-center">
              <ShoppingBag className="w-6 h-6 mr-3 text-blue-500" /> Menu Additions
            </h3>

            <div className="space-y-4">
              {menu.map(item => (
                <div key={item.itemId} className="flex justify-between items-center p-4 bg-gray-50 rounded-2xl hover:bg-gray-100 transition-colors border border-transparent hover:border-gray-200">
                  <div>
                    <h4 className="font-bold text-gray-900 text-lg">{item.name}</h4>
                    <p className="text-sm text-gray-500 line-clamp-1">{item.description}</p>
                    <p className="font-bold text-green-600 mt-1">${item.price.toFixed(2)}</p>
                  </div>
                  
                  <div className="flex items-center space-x-4 bg-white p-2 rounded-xl shadow-sm border border-gray-100">
                    <button onClick={() => updateCart(item.itemId, -1)} className="p-1 rounded-lg hover:bg-gray-100 text-gray-500">
                      <Minus className="w-5 h-5" />
                    </button>
                    <span className="font-bold w-4 text-center">{cart[item.itemId] || 0}</span>
                    <button onClick={() => updateCart(item.itemId, 1)} className="p-1 rounded-lg hover:bg-blue-50 text-blue-600">
                      <Plus className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              ))}

              {menu.length === 0 && (
                <div className="p-8 text-center bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200">
                   <p className="text-gray-500">This restaurant has no active menu items.</p>
                </div>
              )}
            </div>
          </div>

          {/* Cart Section */}
          <div className="md:w-1/3 bg-gray-900 text-white p-8 flex flex-col">
            <h2 className="text-2xl font-bold mb-6">Your Order</h2>
            
            <div className="flex-1 space-y-4 overflow-y-auto mb-6">
              {Object.keys(cart).length === 0 ? (
                <p className="text-gray-400 italic">Your cart is empty.</p>
              ) : (
                Object.entries(cart).map(([itemId, qty]) => {
                  const item = menu.find(m => m.itemId === parseInt(itemId));
                  if (!item) return null;
                  return (
                    <div key={itemId} className="flex justify-between items-center bg-gray-800 p-4 rounded-xl">
                      <div>
                        <p className="font-bold">{item.name}</p>
                        <p className="text-xs text-gray-400">Qty: {qty}</p>
                      </div>
                      <p className="font-bold text-green-400">${(item.price * qty).toFixed(2)}</p>
                    </div>
                  )
                })
              )}
            </div>

            <div className="border-t border-gray-800 pt-6 mt-auto">
              <div className="flex justify-between items-center mb-6">
                <span className="text-gray-400 text-lg">Subtotal</span>
                <span className="text-2xl font-bold">${getSubtotal().toFixed(2)}</span>
              </div>
              <button 
                onClick={handleCheckout}
                disabled={Object.keys(cart).length === 0}
                className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-gray-800 disabled:text-gray-500 text-white py-4 rounded-xl font-bold text-lg flex items-center justify-center transition-colors"
              >
                Checkout <CreditCard className="w-5 h-5 ml-2" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
