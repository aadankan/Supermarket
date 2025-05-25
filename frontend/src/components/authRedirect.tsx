import { Navigate } from "react-router-dom";

import React from "react";

const AuthRedirect: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const token = localStorage.getItem("token");
  console.log(token);
  if (token) {
    return <Navigate to="/" replace />;
  }
  return children;
};

export default AuthRedirect;
