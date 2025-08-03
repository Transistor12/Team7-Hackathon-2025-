import React from 'react';
import Layout from './Layout';

const Settings = ({ user, onLogout }) => {
  return (
    <Layout user={user} onLogout={onLogout} currentPage="settings">
      <div className="page-header">
        <h1 className="page-title">Settings</h1>
      </div>
      
      <div className="under-development">
        <h2>This section is under development.</h2>
        <p>Settings features will be available soon.</p>
      </div>
    </Layout>
  );
};

export default Settings;

