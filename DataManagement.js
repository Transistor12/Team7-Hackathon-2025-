import React from 'react';
import Layout from './Layout';

const DataManagement = ({ user, onLogout }) => {
  return (
    <Layout user={user} onLogout={onLogout} currentPage="data-management">
      <div className="page-header">
        <h1 className="page-title">Data Management</h1>
      </div>
      
      <div className="under-development">
        <h2>This section is under development.</h2>
        <p>Data management features will be available soon.</p>
      </div>
    </Layout>
  );
};

export default DataManagement;

