import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from '@/pages/Login'
import { Navbar } from '@/components/Navbar'
import { Home } from '@/pages/Home'

import './App.css'

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || null);

  return (
    <Router>
      <div className="min-h-screen bg-zinc-50 flex flex-col">
        <Navbar token={token} setToken={setToken} />
        
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route 
              path="/login" 
              element={!token ? <Login setToken={setToken} /> : <Navigate to="/" />} 
            />
            {/* We will add more routes here, like /admin or /restaurant/:id */}
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
