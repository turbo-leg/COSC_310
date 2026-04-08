import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import api from '@/lib/api';

function formatApiError(err) {
  const detail = err?.response?.data?.detail;
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) {
    return detail.map((d) => d.msg || JSON.stringify(d)).join(' ');
  }
  return err?.message || 'Registration failed';
}

export default function Register() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('customer');
  const [restaurantId, setRestaurantId] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const payload = {
      name,
      email,
      password,
      role,
      ...(role === 'restaurant' && restaurantId
        ? { restaurantId: Number(restaurantId) }
        : {}),
    };

    try {
      await api.post('/users/', payload);
      navigate('/login');
    } catch (err) {
      setError(formatApiError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-full items-center justify-center p-4 bg-zinc-50">
      <Card className="w-full max-w-sm">
        <form onSubmit={handleRegister}>
          <CardHeader className="space-y-1">
            <CardTitle className="text-2xl font-bold">Create account</CardTitle>
            <CardDescription>
              Sign up with the same API as <code className="text-xs">POST /users/</code>
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4">
            {error && (
              <div className="text-sm font-medium text-destructive">{error}</div>
            )}
            <div className="grid gap-2 text-left">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div className="grid gap-2 text-left">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="m@example.com"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="grid gap-2 text-left">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                required
                minLength={8}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <p className="text-xs text-muted-foreground">
                At least 8 characters (backend requirement).
              </p>
            </div>
            <div className="grid gap-2 text-left">
              <Label htmlFor="role">Role</Label>
              <select
                id="role"
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                value={role}
                onChange={(e) => setRole(e.target.value)}
              >
                <option value="customer">Customer</option>
                <option value="regular_user">Regular user</option>
                <option value="restaurant">Restaurant owner</option>
              </select>
            </div>
            {role === 'restaurant' && (
              <div className="grid gap-2 text-left">
                <Label htmlFor="restaurantId">Restaurant ID</Label>
                <Input
                  id="restaurantId"
                  type="number"
                  min="1"
                  required
                  value={restaurantId}
                  onChange={(e) => setRestaurantId(e.target.value)}
                />
                <p className="text-xs text-muted-foreground">
                  Must exist in menu data and have no owner yet.
                </p>
              </div>
            )}
            <p className="text-sm text-muted-foreground">
              Already have an account?{' '}
              <Link to="/login" className="underline font-medium text-primary">
                Login
              </Link>
            </p>
          </CardContent>
          <CardFooter>
            <Button className="w-full" type="submit" disabled={loading}>
              {loading ? 'Creating account...' : 'Register'}
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}
