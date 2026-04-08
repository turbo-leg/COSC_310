import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';

export function Navbar({ token, setToken }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('token');
    navigate('/login');
  };

  let userRole = null;
  if (token) {
    try {
      userRole = JSON.parse(atob(token.split('.')[1])).role;
    } catch {
      userRole = null;
    }
  }

  const normalizedRole = userRole
    ? String(userRole).toLowerCase().replace(/\s+/g, '_')
    : null;

  return (
    <nav className="border-b p-4 bg-white shadow-sm flex justify-between items-center">
      <div className="text-xl font-bold">
        <Link to="/" className="text-zinc-900">FoodDelivery</Link>
      </div>
      <div className="flex flex-wrap items-center gap-2 sm:gap-4">
        <Link to="/orders">
          <Button variant="outline">My Orders</Button>
        </Link>
        {!token ? (
          <>
            <Link to="/login">
              <Button variant="default">Login</Button>
            </Link>
            <Link to="/register">
              <Button variant="outline">Register</Button>
            </Link>
          </>
        ) : (
          <>
            {normalizedRole === 'restaurant' && (
              <>
                <Link to="/menu-manager">
                  <Button variant="outline" className="border-blue-200 text-blue-700 bg-blue-50 hover:bg-blue-100">Manage Menu</Button>
                </Link>
                <Link to="/restaurant-orders">
                  <Button variant="outline" className="border-orange-200 text-orange-700 bg-orange-50 hover:bg-orange-100">Restaurant Queue</Button>
                </Link>
              </>
            )}
            {normalizedRole === 'admin' && (
              <Link to="/admin">
                <Button variant="secondary">Admin UI</Button>
              </Link>
            )}
            <Button variant="destructive" onClick={handleLogout}>
              Logout
            </Button>
          </>
        )}
      </div>
    </nav>
  );
}