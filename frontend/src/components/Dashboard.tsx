import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const Dashboard: React.FC = () => {
  const { token, logout } = useAuth();

  return (
    <div>
      <h1>Dashboard</h1>
      <p>You are logged in with the token: {token}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
};

export default Dashboard;
