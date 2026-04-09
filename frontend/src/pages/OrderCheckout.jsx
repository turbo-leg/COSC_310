import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../lib/api';
import { ShoppingBag, ArrowLeft, Plus, Minus, CreditCard, Loader2, Navigation, Clock } from 'lucide-react';

export default function OrderCheckout() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [restaurant, setRestaurant] = useState(null);
  const [menu, setMenu] = useState([]);
  const [cart, setCart] = useState({});
  const [loading, setLoading] = useState(true);
  
  const [distance, setDistance] = useState(3.5);
  const [time, setTime] = useState(20);
  const [totalCost, setTotalCost] = useState(0);

  const token = localStorage.getItem('token');
  const decodedToken = token ? JSON.parse(atob(token.split('.')[1])) : null;
  const userId = decodedToken?.userId;

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

  useEffect(() => {
    // Dynamically calculate the precise price + delivery via the API!
    const calculateTotal = async () => {
      const itemsList = [];
      Object.entries(cart).forEach(([itemId, qty]) => {
        for (let i = 0; i < qty; i++) itemsList.push(parseInt(itemId));
      });

      if (itemsList.length === 0) {
        setTotalCost(0);
        return;
      }

      try {
        const res = await api.post('/orders/calculate-total-cost', {
          item_ids: itemsList,
          distance_km: distance || 0.1,
          time_minutes: time || 1
        });
        setTotalCost(res.data.total_order_cost);
      } catch (err) {
        console.error("Failed to calculate total cost via API");
      }
    };

    const timer = setTimeout(calculateTotal, 300); // debounce API calls
    return () => clearTimeout(timer);
  }, [cart, distance, time]);

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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-muted text-muted-foreground">
        <Loader2 className="w-12 h-12 text-blue-500 animate-spin" />
      </div>
    );
  }

  if (!restaurant) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-muted text-muted-foreground p-6">
        <h2 className="text-2xl font-bold mb-4">Restaurant Not Found</h2>
        <button onClick={() => navigate('/')} className="bg-primary text-primary-foreground text-primary-foreground px-6 py-2 rounded-full font-bold">
          Back to Home
        </button>
      </div>
    );
  }

  const handleCheckout = async () => {
    if (!token) {
       alert("Please login before placing an order.");
       navigate('/login');
       return;
    }

    const itemsList = [];
    Object.entries(cart).forEach(([itemId, qty]) => {
      for (let i = 0; i < qty; i++) itemsList.push(parseInt(itemId));
    });

    try {
      const payload = {
        user_id: userId,
        restaurant_id: parseInt(id),
        items: itemsList,
        distance_km: distance || 0.1,
        time_minutes: time || 1
      };

      const res = await api.post('/orders/', payload);
      setCart({});
      navigate(`/payment/${res.data.orderId}`, { state: { amount: totalCost } });
    } catch (err) {
      console.error("Order failed", err);
      alert("Failed to submit order.");
    }
  };

  return (
    <div className="min-h-screen bg-muted text-muted-foreground py-10 px-4 md:px-12 animate-in fade-in duration-500">
      <div className="max-w-5xl mx-auto">
        <button 
          onClick={() => navigate('/')}
          className="flex items-center text-muted-foreground hover:text-blue-600 mb-8 transition-colors font-medium"
        >
          <ArrowLeft className="w-5 h-5 mr-2" /> Back to Restaurants
        </button>

        <div className="bg-card text-card-foreground rounded-[2rem] shadow-sm border border-border overflow-hidden flex flex-col md:flex-row">
          
          {/* Menu Section */}
          <div className="md:w-2/3 p-8 border-r border-border">
            <h1 className="text-4xl font-extrabold text-foreground mb-8">{restaurant.name}</h1>
            
            <h3 className="text-xl font-bold mb-6 text-foreground flex items-center">
              <ShoppingBag className="w-6 h-6 mr-3 text-blue-500" /> Menu Additions
            </h3>

            <div className="space-y-4">
              {menu.map(item => (
                <div key={item.itemId} className="flex flex-col sm:flex-row justify-between sm:items-center p-4 bg-muted text-muted-foreground rounded-2xl hover:bg-muted transition-colors border border-transparent hover:border-border gap-4">
                  <div>
                    <h4 className="font-bold text-foreground text-lg">{item.name}</h4>
                    <p className="text-sm text-muted-foreground line-clamp-1">{item.description}</p>
                    <p className="font-bold text-green-600 mt-1">${item.price.toFixed(2)}</p>
                  </div>
                  
                  <div className="flex items-center space-x-4 bg-card text-card-foreground p-2 rounded-xl shadow-sm border border-border self-start sm:self-auto shrink-0">
                    <button onClick={() => updateCart(item.itemId, -1)} className="p-1 rounded-lg hover:bg-muted text-muted-foreground transition-colors">
                      <Minus className="w-5 h-5" />
                    </button>
                    <span className="font-bold w-6 text-center">{cart[item.itemId] || 0}</span>
                    <button onClick={() => updateCart(item.itemId, 1)} className="p-1 rounded-lg hover:bg-secondary/10 text-blue-600 transition-colors">
                      <Plus className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              ))}

              {menu.length === 0 && (
                <div className="p-8 text-center bg-muted text-muted-foreground rounded-2xl border-2 border-dashed border-border">
                   <p className="text-muted-foreground font-medium">This restaurant has no active menu items.</p>
                </div>
              )}
            </div>
          </div>

          {/* Cart Section */}
          <div className="md:w-1/3 bg-primary text-primary-foreground text-primary-foreground p-8 flex flex-col relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-secondary/100 opacity-10 rounded-bl-[100px] pointer-events-none" />
            <h2 className="text-2xl font-bold mb-6">Your Order</h2>
            
            <div className="flex-1 space-y-4 overflow-y-auto mb-6 relative z-10">
              {Object.keys(cart).length === 0 ? (
                <p className="text-muted-foreground italic">Your cart is empty.</p>
              ) : (
                <>
                  {Object.entries(cart).map(([itemId, qty]) => {
                    const item = menu.find(m => m.itemId === parseInt(itemId));
                    if (!item) return null;
                    return (
                      <div key={itemId} className="flex justify-between items-center bg-secondary text-secondary-foreground/50 p-4 rounded-xl border border-border/50">
                        <div>
                          <p className="font-bold text-sm">{item.name}</p>
                          <p className="text-xs text-muted-foreground">Qty: {qty}</p>
                        </div>
                        <p className="font-bold text-green-400 text-sm">${(item.price * qty).toFixed(2)}</p>
                      </div>
                    )
                  })}
                  
                  {/* Delivery Adjustments Input */}
                  <div className="mt-8 bg-secondary text-secondary-foreground p-5 rounded-2xl shadow-inner border border-border">
                    <h4 className="text-sm font-bold text-blue-400 uppercase tracking-widest mb-4">Delivery Route</h4>
                    
                    <div className="space-y-4">
                      <div>
                        <label className="flex items-center text-xs font-bold text-muted-foreground mb-1.5"><Navigation className="w-3 h-3 mr-1.5"/> Distance (km)</label>
                        <input 
                          type="number" min="0.1" step="0.1"
                          value={distance} onChange={e => setDistance(parseFloat(e.target.value))}
                          className="w-full bg-primary text-primary-foreground text-primary-foreground text-sm px-4 py-2.5 rounded-lg border border-border focus:border-primary-500 focus:ring-1 focus:ring-primary-500 outline-none"
                        />
                      </div>
                      <div>
                        <label className="flex items-center text-xs font-bold text-muted-foreground mb-1.5"><Clock className="w-3 h-3 mr-1.5"/> ETA Config (mins)</label>
                        <input 
                          type="number" min="1" step="1"
                          value={time} onChange={e => setTime(parseInt(e.target.value))}
                          className="w-full bg-primary text-primary-foreground text-primary-foreground text-sm px-4 py-2.5 rounded-lg border border-border focus:border-primary-500 focus:ring-1 focus:ring-primary-500 outline-none"
                        />
                      </div>
                    </div>
                  </div>
                </>
              )}
            </div>

            <div className="border-t border-border pt-6 mt-auto relative z-10">
              <div className="flex justify-between items-center mb-6">
                <span className="text-muted-foreground text-lg">Total</span>
                <div className="text-right">
                  <span className="text-3xl font-black text-primary-foreground">${totalCost.toFixed(2)}</span>
                  <p className="text-xs text-blue-400 mt-1 font-medium select-none">API Price Engine</p>
                </div>
              </div>
              <button 
                onClick={handleCheckout}
                disabled={Object.keys(cart).length === 0}
                className="w-full bg-primary text-primary-foreground hover:bg-secondary/100 disabled:bg-secondary text-secondary-foreground disabled:text-muted-foreground disabled:border-transparent text-primary-foreground py-4 rounded-xl font-bold text-lg flex items-center justify-center transition-all shadow-lg hover:shadow-blue-500/20 border border-primary-500"
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
