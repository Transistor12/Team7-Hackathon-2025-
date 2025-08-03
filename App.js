import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import Dashboard from './components/Dashboard';
import UserManagement from './components/UserManagement';
import Analytics from './components/Analytics';
import DataManagement from './components/DataManagement';
import Settings from './components/Settings';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  const handleLogin = (userData) => {
    setIsAuthenticated(true);
    setUser(userData);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route 
            path="/" 
            element={
              isAuthenticated ? 
              <Navigate to="/dashboard" replace /> : 
              <LoginPage onLogin={handleLogin} />
            } 
          />
          <Route 
            path="/dashboard" 
            element={
              isAuthenticated ? 
              <Dashboard user={user} onLogout={handleLogout} /> : 
              <Navigate to="/" replace />
            } 
          />
          <Route 
            path="/user-management" 
            element={
              isAuthenticated ? 
              <UserManagement user={user} onLogout={handleLogout} /> : 
              <Navigate to="/" replace />
            } 
          />
          <Route 
            path="/analytics" 
            element={
              isAuthenticated ? 
              <Analytics user={user} onLogout={handleLogout} /> : 
              <Navigate to="/" replace />
            } 
          />
          <Route 
            path="/data-management" 
            element={
              isAuthenticated ? 
              <DataManagement user={user} onLogout={handleLogout} /> : 
              <Navigate to="/" replace />
            } 
          />
          <Route 
            path="/settings" 
            element={
              isAuthenticated ? 
              <Settings user={user} onLogout={handleLogout} /> : 
              <Navigate to="/" replace />
            } 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

