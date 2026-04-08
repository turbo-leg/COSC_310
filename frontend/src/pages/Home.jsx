import React, { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export function Home() {
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/restaurants')
      .then(res => res.json())
      .then(data => setRestaurants(data))
      .catch(err => console.error("Error fetching restaurants", err));
  }, []);

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Available Restaurants</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {restaurants.map(r => (
          <Card key={r.userId} className="flex flex-col justify-between">
            <CardHeader>
              <CardTitle>{r.name}</CardTitle>
              <CardDescription>Role: {r.role}</CardDescription>
            </CardHeader>
            <CardContent>
              <Button className="w-full">View Menu</Button>
            </CardContent>
          </Card>
        ))}
        {restaurants.length === 0 && (
          <p className="text-zinc-500">No restaurants currently available.</p>
        )}
      </div>
    </div>
  );
}