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

  const userRole = token ? JSON.parse(atob(token.split('.')[1])).role : null;

  return (
    <nav className="border-b p-4 bg-white shadow-sm flex justify-between items-center">
      <div className="text-xl font-bold">
        <Link to="/" className="text-zinc-900">FoodDelivery</Link>
      </div>
      <div className="flex gap-4">
        {!token ? (
          <Link to="/login">
            <Button variant="outline">Login</Button>
          </Link>
        ) : (
          <>
            {userRole === 'admin' && (
              <Link to="/admin">
                <Button variant="secondary">Admin Dashboard</Button>
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