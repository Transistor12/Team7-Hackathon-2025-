import React from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from './Layout';
import { Users, BarChart3, Database, Settings } from 'lucide-react';

const Dashboard = ({ user, onLogout }) => {
  const navigate = useNavigate();

  const dashboardCards = [
    {
      icon: Users,
      title: 'User Management',
      description: 'Manage farmers, buyers, and data ambassadors',
      color: 'user-management',
      onClick: () => navigate('/user-management')
    },
    {
      icon: BarChart3,
      title: 'System Analytics',
      description: 'View platform usage and performance metrics',
      color: 'analytics',
      onClick: () => navigate('/analytics')
    },
    {
      icon: Database,
      title: 'Data Management',
      description: 'Oversee agricultural data and market information',
      color: 'data-management',
      onClick: () => navigate('/data-management')
    },
    {
      icon: Settings,
      title: 'Platform Settings',
      description: 'Configure system settings and preferences',
      color: 'settings',
      onClick: () => navigate('/settings')
    }
  ];

  const stats = [
    {
      label: 'Total Users',
      value: '1,247',
      change: '+12% from last month',
      color: 'users'
    },
    {
      label: 'Active Farmers',
      value: '892',
      change: '+8% from last month',
      color: 'farmers'
    },
    {
      label: 'Data Ambassadors',
      value: '45',
      change: '+15% from last month',
      color: 'ambassadors'
    }
  ];

  return (
    <Layout user={user} onLogout={onLogout} currentPage="dashboard">
      <div className="page-header">
        <h1 className="page-title">Admin Dashboard</h1>
        <p className="page-description">Manage and oversee the HarvestNet platform</p>
      </div>

      <div className="dashboard-grid">
        {dashboardCards.map((card, index) => (
          <div key={index} className="dashboard-card" onClick={card.onClick} style={{ cursor: 'pointer' }}>
            <div className="dashboard-card-header">
              <div className={`dashboard-card-icon ${card.color}`}>
                <card.icon size={24} />
              </div>
              <h3 className="dashboard-card-title">{card.title}</h3>
            </div>
            <p className="dashboard-card-description">{card.description}</p>
            <button className="btn btn-secondary">Learn more</button>
          </div>
        ))}
      </div>

      <div className="stats-section">
        {stats.map((stat, index) => (
          <div key={index} className="stat-card">
            <div className={`stat-value ${stat.color}`}>{stat.value}</div>
            <div className="stat-label">{stat.label}</div>
            <div className="stat-change">{stat.change}</div>
          </div>
        ))}
      </div>
    </Layout>
  );
};

export default Dashboard;

