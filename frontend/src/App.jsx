import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'

import Login from '@/pages/Login'
import Register from '@/pages/Register'
import { Navbar } from '@/components/Navbar'
import { Home } from '@/pages/Home'
import OrderCheckout from '@/pages/OrderCheckout'
import AdminDashboard from '@/pages/AdminDashboard'
import CheckoutPayment from '@/pages/CheckoutPayment'
import UserOrders from '@/pages/UserOrders'
import RestaurantOrders from '@/pages/RestaurantOrders'
import OrderTracker from '@/pages/OrderTracker'
import DeliveryManager from '@/pages/DeliveryManager'
import RestaurantMenuManager from '@/pages/RestaurantMenuManager'
import WalletPage from '@/pages/Wallet'

import './App.css'

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [isDarkMode, setIsDarkMode] = useState(() => {
    return localStorage.getItem('theme') === 'dark' ||
      (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
  });

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDarkMode]);

  const toggleTheme = () => setIsDarkMode(prev => !prev);

  return (
    <Router>
      <div className="min-h-screen bg-background text-foreground flex flex-col transition-colors duration-300">
        <Navbar token={token} setToken={setToken} toggleTheme={toggleTheme} isDarkMode={isDarkMode} />
        
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route 
              path="/login" 
              element={!token ? <Login setToken={setToken} /> : <Navigate to="/" />} 
            />
            <Route
              path="/register"
              element={!token ? <Register /> : <Navigate to="/" />}
            />
            <Route path="/restaurant/:id" element={<OrderCheckout />} />
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/payment/:orderId" element={<CheckoutPayment />} />
            <Route
              path="/orders"
              element={token ? <UserOrders /> : <Navigate to="/login" replace />}
            />
            <Route path="/restaurant-orders" element={<RestaurantOrders />} />
            <Route path="/menu-manager" element={<RestaurantMenuManager />} />
            <Route path="/order/:id/track" element={<OrderTracker />} />
            <Route path="/dispatch" element={<DeliveryManager />} />
            <Route
              path="/wallet"
              element={token ? <WalletPage /> : <Navigate to="/login" replace />}
            />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
