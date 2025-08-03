import React from 'react';
import Layout from './Layout';

const UserManagement = ({ user, onLogout }) => {
  return (
    <Layout user={user} onLogout={onLogout} currentPage="user-management">
      <div className="page-header">
        <h1 className="page-title">User Management</h1>
      </div>
      
      <div className="under-development">
        <h2>This section is under development.</h2>
        <p>User management features will be available soon.</p>
      </div>
    </Layout>
  );
};

export default UserManagement;

