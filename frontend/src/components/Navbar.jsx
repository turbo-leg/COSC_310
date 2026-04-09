import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button, buttonVariants } from '@/components/ui/button';
import { Cat, Moon, Sun } from 'lucide-react';

export function Navbar({ token, setToken, toggleTheme, isDarkMode }) {
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
  const canUseWallet = normalizedRole === 'customer' || normalizedRole === 'regular_user';

  return (
    <nav className="border-b p-4 bg-background shadow-sm flex justify-between items-center transition-colors duration-300">
      <div className="text-xl font-bold flex items-center gap-2">
        <Cat className="text-primary w-6 h-6" strokeWidth={2.5} />
        <Link to="/" className="text-primary tracking-wide">Sphinx Delivery</Link>
      </div>
      <div className="flex flex-wrap items-center gap-2 sm:gap-4">
        <Button variant="ghost" size="icon" onClick={toggleTheme} className="text-foreground transition-colors hover:bg-accent">
          {isDarkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
        </Button>
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
            {canUseWallet && (
              <Link to="/wallet" className={buttonVariants({ variant: 'outline' })}>
                Wallet
              </Link>
            )}
            {normalizedRole === 'restaurant' && (
              <>
                <Link to="/menu-manager">
                  <Button variant="outline" className="border-secondary/20 text-secondary bg-secondary/10 hover:bg-secondary/20">Manage Menu</Button>
                </Link>
                <Link to="/restaurant-orders">
                  <Button variant="outline" className="border-accent/20 text-accent-foreground bg-accent/10 hover:bg-accent/20">Restaurant Queue</Button>
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