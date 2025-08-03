import React, { useState } from 'react';
import { 
  Cloud, 
  TrendingUp, 
  ShoppingCart, 
  Users, 
  Mail, 
  Phone, 
  Eye, 
  EyeOff,
  CheckCircle 
} from 'lucide-react';

const LoginPage = ({ onLogin }) => {
  const [authMethod, setAuthMethod] = useState('email');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Simple authentication check
    if ((email === 'admin@harvestnet.com' && password === 'password123') ||
        (email === 'farmer@harvestnet.com' && password === 'password123')) {
      onLogin({
        name: email === 'admin@harvestnet.com' ? 'Admin User' : 'Farmer User',
        email: email,
        role: email === 'admin@harvestnet.com' ? 'Administrator' : 'Farmer'
      });
    } else {
      alert('Invalid credentials. Please use the demo credentials provided.');
    }
  };

  const features = [
    {
      icon: Cloud,
      title: 'Weather Insights',
      description: 'Get accurate weather forecasts and farming recommendations',
      color: 'weather'
    },
    {
      icon: TrendingUp,
      title: 'Market Prices',
      description: 'Real-time commodity prices from local markets',
      color: 'market'
    },
    {
      icon: ShoppingCart,
      title: 'Marketplace',
      description: 'Buy and sell directly with other farmers',
      color: 'marketplace'
    },
    {
      icon: Users,
      title: 'Community',
      description: 'Connect with cooperatives and local farmers',
      color: 'community'
    }
  ];

  return (
    <div className="login-container">
      <div className="login-left">
        <div className="logo">
          <div className="logo-icon">
            <CheckCircle size={24} />
          </div>
          <div>
            <div className="logo-text">HarvestNet</div>
            <div className="logo-subtitle">Agricultural Platform for Kenyan Farmers</div>
          </div>
        </div>
        
        <h1 className="hero-title">
          Your agricultural companion for better farming decisions
        </h1>
        
        <p className="hero-description">
          Connect with farmers, access real-time weather data, get market prices, 
          and grow your agricultural business with our comprehensive platform.
        </p>
        
        <div className="features-grid">
          {features.map((feature, index) => (
            <div key={index} className="feature-card">
              <div className={`feature-icon ${feature.color}`}>
                <feature.icon size={24} />
              </div>
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>
              <button className="learn-more-btn">Learn more</button>
            </div>
          ))}
        </div>
      </div>
      
      <div className="login-right">
        <div className="login-form-container">
          <form className="login-form" onSubmit={handleSubmit}>
            <h2 className="login-title">Login</h2>
            <p className="login-subtitle">Welcome back to HarvestNet</p>
            
            <div className="auth-toggle">
              <button
                type="button"
                className={`auth-toggle-btn ${authMethod === 'email' ? 'active' : ''}`}
                onClick={() => setAuthMethod('email')}
              >
                <Mail size={16} />
                Email
              </button>
              <button
                type="button"
                className={`auth-toggle-btn ${authMethod === 'phone' ? 'active' : ''}`}
                onClick={() => setAuthMethod('phone')}
              >
                <Phone size={16} />
                Phone Number
              </button>
            </div>
            
            <div className="form-group">
              <label className="label">Email</label>
              <input
                type="email"
                className="input"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            
            <div className="form-group">
              <label className="label">Password</label>
              <div style={{ position: 'relative' }}>
                <input
                  type={showPassword ? 'text' : 'password'}
                  className="input"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  style={{ paddingRight: '48px' }}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    position: 'absolute',
                    right: '12px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    color: '#6b7280'
                  }}
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>
            
            <button type="submit" className="btn btn-primary w-full">
              Login
            </button>
            
            <a href="#" className="forgot-password">Forgot Password?</a>
            
            <div className="register-link">
              Don't have an account? <a href="#">Register</a>
            </div>
            
            <div className="demo-credentials">
              <h4>Demo Credentials:</h4>
              <p>Admin: admin@harvestnet.com / password123</p>
              <p>Farmer: farmer@harvestnet.com / password123</p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;

