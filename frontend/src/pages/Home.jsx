import {
  AlertCircle,
  ArrowRight,
  ChevronDown,
  ChevronUp,
  Crown,
  Search,
  SearchX,
  ShoppingBag,
  Store,
  Utensils,
} from 'lucide-react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../lib/api';

/** Restaurant owner id from JWT (same as restaurantId for owners). */
function getOwnedRestaurantIdFromToken() {
  const token = localStorage.getItem('token');
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    if (payload.role !== 'restaurant') return null;
    const rid = payload.restaurantId ?? payload.userId;
    if (rid === undefined || rid === null) return null;
    const n = Number(rid);
    return Number.isFinite(n) ? n : null;
  } catch {
    return null;
  }
}

export function Home() {
  const [restaurants, setRestaurants] = useState([]);
  const [menus, setMenus] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState('');
  const [expandedId, setExpandedId] = useState(null);
  const navigate = useNavigate();
  const ownedRestaurantId = getOwnedRestaurantIdFromToken();

  const fetchRestaurants = async (searchQuery = '') => {
    try {
      setLoading(true);
      const res = await api.get('/restaurants', { params: { query: searchQuery } });
      setRestaurants(res.data);
      setError(null);
    } catch (err) {
      console.error("Error fetching restaurants", err);
      setError("Failed to load restaurants. Please ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const fetchMenu = async (restaurantId) => {
    if (menus[restaurantId]) return; // Already fetched
    try {
      const res = await api.get(`/restaurant/${restaurantId}/menu`);
      setMenus(prev => ({ ...prev, [restaurantId]: res.data }));
    } catch (err) {
      console.error("Error fetching menu", err);
    }
  };

  useEffect(() => {
    fetchRestaurants();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchRestaurants(query);
  };

  const toggleExpand = (id) => {
    if (expandedId === id) {
      setExpandedId(null);
    } else {
      setExpandedId(id);
      fetchMenu(id);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-12">
      <div className="max-w-6xl mx-auto space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
        
        {/* Header Section */}
        <div className="text-center space-y-4">
          <div className="w-16 h-16 bg-sky-100 text-sky-500 rounded-2xl flex items-center justify-center mx-auto mb-6 border border-blue-200/50 shadow-sm transition-transform hover:scale-105">
            <Utensils className="w-8 h-8" />
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-gray-900 bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-700 pb-2">
            Discover Great Places
          </h1>
          <p className="text-gray-500 text-xl max-w-3xl mx-auto">
            Search our selection of top-tier restaurants and explore their menus instantly.
          </p>
        </div>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="max-w-3xl mx-auto relative group">
          <div className="absolute inset-y-0 left-6 flex items-center pointer-events-none">
            <Search className="h-6 w-6 text-gray-400 group-hover:text-blue-500 transition-colors" />
          </div>
          <input
            type="text"
            className="block w-full p-5 pl-16 text-lg text-gray-900 border border-gray-200 rounded-full bg-white shadow-sm focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all placeholder-gray-400"
            placeholder="Search for restaurants..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button 
            type="submit" 
            className="absolute right-3 top-2.5 bottom-2.5 px-6 font-semibold bg-zinc-800 hover:bg-black text-white rounded-full transition-colors flex items-center shadow-md hover:shadow-lg transform active:scale-95"
          >
            Search
          </button>
        </form>

        {/* States Section */}
        {loading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-56 bg-white rounded-3xl border border-gray-100 shadow-sm p-6 flex flex-col justify-between">
                 <div className="flex gap-4">
                   <div className="w-12 h-12 bg-gray-200 rounded-xl"></div>
                   <div className="flex-1 space-y-2">
                     <div className="h-5 bg-gray-200 rounded w-3/4"></div>
                     <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                   </div>
                 </div>
              </div>
            ))}
          </div>
        )}

        {error && !loading && (
          <div className="flex flex-col items-center justify-center p-12 bg-red-50 text-red-700 rounded-3xl border border-red-100">
            <AlertCircle className="w-12 h-12 text-red-500 mb-4" />
            <p className="font-semibold text-lg text-center">{error}</p>
          </div>
        )}

        {/* Content Section */}
        {!loading && !error && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {restaurants.map(r => {
              const rid = r.restaurantId ?? r.userId;
              const isMine = ownedRestaurantId !== null && Number(rid) === ownedRestaurantId;
              return (
              <div 
                key={rid} 
                className={`bg-white rounded-3xl shadow-sm hover:shadow-xl border border-gray-100 transition-all duration-500 overflow-hidden ${expandedId === rid ? 'ring-2 ring-blue-500/20' : ''}`}
              >
                <div 
                  className="p-6 cursor-pointer relative group flex flex-col justify-between"
                  onClick={() => toggleExpand(rid)}
                >
                  <div className="absolute top-0 right-0 w-48 h-48 bg-gradient-to-br from-blue-50/50 to-purple-50/50 rounded-bl-full -z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                  
                  <div>
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-4">
                        <div className="p-3 bg-gray-50 text-gray-700 rounded-2xl group-hover:bg-blue-50 group-hover:text-sky-600 transition-colors border border-gray-100 group-hover:border-blue-100 shadow-sm">
                          <Store className="w-7 h-7" />
                        </div>
                        <div className="flex items-center gap-2 flex-wrap">
                          <h3 className="text-2xl font-bold text-zinc-800 leading-tight pb-1">{r.name}</h3>
                          {isMine && (
                            <span
                              className="inline-flex items-center gap-1 rounded-full bg-amber-100 text-amber-900 px-2.5 py-0.5 text-xs font-semibold border border-amber-200"
                              title="Your restaurant"
                            >
                              <Crown className="w-3.5 h-3.5" aria-hidden />
                              Yours
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="mt-4 flex items-center justify-between pt-4 border-t border-gray-50">
                    <div 
                      className="flex items-center gap-2 text-sm font-medium text-gray-500 hover:text-blue-600 transition-colors z-10 cursor-pointer p-2 -ml-2"
                      onClick={(e) => { e.stopPropagation(); toggleExpand(rid); }}
                    >
                      {expandedId === rid ? 'Hide Menu' : 'View Menu'}
                      {expandedId === rid ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </div>
                    <button 
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/restaurant/${rid}`);
                      }}
                      className="flex items-center gap-2 bg-gray-50 hover:bg-sky-500 hover:shadow-lg text-gray-700 hover:text-white py-2 px-4 rounded-xl font-medium transition-all"
                    >
                      Order Now <ArrowRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Expanded Menu Section */}
                <div 
                  className={`overflow-hidden transition-all duration-500 ease-in-out bg-gray-50 ${
                    expandedId === rid ? 'max-h-screen opacity-100 border-t border-gray-100' : 'max-h-0 opacity-0'
                  }`}
                >
                  <div className="p-6">
                    <h4 className="text-sm font-bold text-gray-900 uppercase tracking-widest mb-4 flex items-center gap-2">
                       <ShoppingBag className="w-4 h-4 text-gray-400" /> Menu Items
                    </h4>
                    
                    {!menus[rid] ? (
                      <div className="animate-pulse flex gap-4 p-4 bg-white rounded-xl">
                        <div className="w-16 h-16 bg-gray-200 rounded-lg"></div>
                        <div className="flex-1 space-y-2 py-1">
                          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                          <div className="h-3 bg-gray-200 rounded w-1/4"></div>
                        </div>
                      </div>
                    ) : menus[rid].length === 0 ? (
                      <div className="text-center py-6 bg-white rounded-2xl border border-gray-100 border-dashed">
                        <p className="text-sm text-gray-500">This restaurant hasn't added any menu items yet.</p>
                      </div>
                    ) : (
                      <div className="space-y-3 max-h-80 overflow-y-auto pr-2 custom-scrollbar">
                        {menus[rid].map(item => (
                          <div key={item.itemId ?? item.item_id} className="group/item flex items-center justify-between p-4 bg-white rounded-2xl border border-gray-100 hover:border-blue-200 hover:shadow-md transition-all">
                            <div>
                              <h5 className="font-bold text-gray-900 group-hover/item:text-blue-700 transition-colors">{item.name}</h5>
                              <p className="text-sm text-gray-500 line-clamp-1 mt-0.5">{item.description}</p>
                            </div>
                            <span className="font-extrabold text-gray-900 bg-gray-50 px-3 py-1.5 rounded-lg border border-gray-100">
                              ${item.price.toFixed(2)}
                            </span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

              </div>
            );
            })}

            {restaurants.length === 0 && (
              <div className="col-span-1 lg:col-span-2 flex flex-col items-center justify-center text-center p-16 md:p-24 bg-white border border-gray-100 rounded-[2.5rem] shadow-sm">
                <div className="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mb-6 border border-gray-100">
                  <SearchX className="w-10 h-10 text-gray-400" />
                </div>
                <h3 className="text-3xl font-bold text-gray-900 mb-3">No Results Found</h3>
                <p className="text-gray-500 text-lg max-w-md mx-auto">
                  {query 
                    ? `We couldn't find any restaurants matching "${query}". Try different keywords.`
                    : "There are currently no active restaurants in the system. Check back soon!"}
                </p>
                {query && (
                  <button 
                    onClick={() => { setQuery(''); fetchRestaurants(''); }}
                    className="mt-8 px-6 py-3 bg-white border-2 border-gray-200 text-gray-700 font-bold rounded-full hover:bg-gray-50 hover:border-gray-300 transition-all"
                  >
                    Clear Search
                  </button>
                )}
              </div>
            )}
          </div>
        )}
      </div>
      
      {/* Custom Scrollbar CSS embedded for convenience */}
      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #f1f5f9;
          border-radius: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #cbd5e1;
          border-radius: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #94a3b8;
        }
      `}</style>
    </div>
  );
}