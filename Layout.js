import React from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Home, 
  Users, 
  BarChart3, 
  Database, 
  Settings, 
  CheckCircle,
  LogOut,
  Globe
} from 'lucide-react';

const Layout = ({ children, user, onLogout, currentPage }) => {
  const navigate = useNavigate();

  const navigationItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: Home,
      path: '/dashboard'
    },
    {
      id: 'user-management',
      label: 'User Management',
      icon: Users,
      path: '/user-management'
    },
    {
      id: 'analytics',
      label: 'Analytics',
      icon: BarChart3,
      path: '/analytics'
    },
    {
      id: 'data-management',
      label: 'Data Management',
      icon: Database,
      path: '/data-management'
    },
    {
      id: 'settings',
      label: 'Settings',
      icon: Settings,
      path: '/settings'
    }
  ];

  const handleNavigation = (path) => {
    navigate(path);
  };

  const handleLogout = () => {
    onLogout();
    navigate('/');
  };

  return (
    <div className="dashboard-layout">
      <div className="sidebar">
        <div className="sidebar-header">
          <div className="logo">
            <div className="logo-icon">
              <CheckCircle size={20} />
            </div>
            <div>
              <div className="logo-text" style={{ fontSize: '18px' }}>HarvestNet</div>
              <div className="logo-subtitle">Agricultural Platform for Kenyan Farmers</div>
            </div>
          </div>
        </div>

        <nav className="sidebar-nav">
          {navigationItems.map((item) => (
            <button
              key={item.id}
              className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
              onClick={() => handleNavigation(item.path)}
            >
              <item.icon className="nav-icon" size={20} />
              {item.label}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="user-profile">
            <div className="user-avatar">
              {user?.name?.charAt(0) || 'A'}
            </div>
            <div className="user-info">
              <div className="user-name">{user?.name || 'Admin User'}</div>
              <div className="user-role">{user?.role || 'Administrator'}</div>
            </div>
          </div>
        </div>
      </div>

      <div className="main-content">
        <div className="top-bar">
          <div className="top-bar-left">
            {/* Additional top bar content can go here */}
          </div>
          <div className="top-bar-right">
            <button className="language-selector">
              <Globe size={16} style={{ marginRight: '8px' }} />
              EN
            </button>
            <button className="logout-btn" onClick={handleLogout}>
              <LogOut size={16} style={{ marginRight: '8px' }} />
              Logout
            </button>
          </div>
        </div>
        
        {children}
      </div>
    </div>
  );
};

export default Layout;

