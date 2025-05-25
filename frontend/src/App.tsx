import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainPage from './pages/index';
import LoginPage from './pages/account/LoginPage';
import RegisterPage from './pages/account/RegisterPage';
import Store from './pages/Store';

import AuthRedirect from './components/authRedirect';
import PrivateRoute from './components/privateRoute';

function App() {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Store />
            </PrivateRoute>
          }
        />

        <Route
          path="/login"
          element={
            <AuthRedirect>
              <LoginPage />
            </AuthRedirect>
          }
        />
        <Route
          path="/register"
          element={
            <AuthRedirect>
              <RegisterPage />
            </AuthRedirect>
          }
        />
        <Route path="*" element={<MainPage />} />
      </Routes>
    </Router>
  );
}

export default App;
