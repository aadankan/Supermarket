import { Navigate } from 'react-router-dom';

import React from 'react';

const PrivateRoute: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const token = localStorage.getItem('token');
  if (!token) {
    return <Navigate to="/start-page" />;
  }
  return children;
};

export default PrivateRoute;
