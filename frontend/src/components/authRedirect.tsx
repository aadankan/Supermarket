import { Navigate } from "react-router-dom";

const AuthRedirect = ({ children }) => {
  const token = localStorage.getItem("token");
  console.log(token);
  if (token) {
    return <Navigate to="/" replace />;
  }
  return children;
};

export default AuthRedirect;
