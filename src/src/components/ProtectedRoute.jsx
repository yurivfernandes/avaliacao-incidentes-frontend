import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  const token = localStorage.getItem('token');

  if (loading) {
    return <div>Carregando...</div>; // Exibe uma mensagem enquanto o estado de autenticação é resolvido
  }

  if (!token || !user) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
