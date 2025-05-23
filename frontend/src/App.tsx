// App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainPage from './pages/index';
import LoginPage from './pages/account/LoginPage';
import RegisterPage from './pages/account/RegisterPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Routes>
    </Router>
  );
}

export default App;
