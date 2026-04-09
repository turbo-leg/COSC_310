import { Button } from '@/components/ui/button';
import { Link, useNavigate } from 'react-router-dom';

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
    <nav className="border-b p-7 bg-gradient-to-r from-sky-500 to-sky-400 shadow-2xl flex justify-between items-center">
      <div className="text-xl font-bold">
        <Link to="/" className="text-white text-2xl">FoodDelivery</Link>
      </div>
      <div className="flex flex-wrap items-center gap-2 sm:gap-4">
        <Link to="/orders">
          <Button variant="ghost" className = "text-xl text-white" >My Orders</Button>
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
            <Button variant="destructive" onClick={handleLogout} className = "text-xl text-zinc-800">
              Logout
            </Button>
          </>
        )}
      </div>
    </nav>
  );
}