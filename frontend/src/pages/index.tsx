import supermarket from "../assets/images/SupermarketEntrance.png";
import { useNavigate } from "react-router-dom";
import LoginButton from "../components/account.tsx/LoginButton";
import RegisterButton from "../components/account.tsx/RegisterButton";
import AdminPanel from "../components/account.tsx/AdminPanel";

const MainPage = () => {
  const navigate = useNavigate();

  const login = () => {
    navigate("/login");
  };

  const register = () => {
    navigate("/register")
  };

  const adminPanel = () => {
    console.log("Admin panel clicked");
  };

  return (
    <div
      style={{ backgroundImage: `url(${supermarket})` }}
      className="bg-cover bg-bottom h-screen"
    >
      <AdminPanel adminPanel={adminPanel} />
      <div className="w-full h-[calc(100%-160px)] flex justify-center items-center gap-40 overflow-hidden">
        <LoginButton login={login} />
        <RegisterButton register={register} />
      </div>
    </div>
  );
};

export default MainPage;
