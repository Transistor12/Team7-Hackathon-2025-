import React from 'react';
import Layout from './Layout';

const Analytics = ({ user, onLogout }) => {
  return (
    <Layout user={user} onLogout={onLogout} currentPage="analytics">
      <div className="page-header">
        <h1 className="page-title">Analytics</h1>
      </div>
      
      <div className="under-development">
        <h2>This section is under development.</h2>
        <p>Analytics features will be available soon.</p>
      </div>
    </Layout>
  );
};

export default Analytics;

