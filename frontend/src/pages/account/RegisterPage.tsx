import { useNavigate } from "react-router-dom";
import supermarket from "../../assets/images/SupermarketEntrance.png";
import AdminPanel from "../../components/account.tsx/AdminPanel";
import Email from "../../components/account.tsx/Email";
import Password from "../../components/account.tsx/Password";
import RegisterSign from "../../components/account.tsx/RegisterSign";

const RegisterPage = () => {
  const navigate = useNavigate();

  const login = () => {
    console.log("login");
  };

  const register = () => {
    navigate("/register");
  };

  const adminPanel = () => {
    console.log("adminPanel");
  };

  return (
    <div
      style={{ backgroundImage: `url(${supermarket})` }}
      className="bg-cover bg-bottom h-screen"
    >
      <AdminPanel adminPanel={adminPanel} />
      <div className="w-full h-[calc(100%-160px)] flex justify-center items-center gap-40 overflow-hidden">
        <div className="w-[510px] p-7 bg-white/60 rounded-[48px] shadow-[0px_2.4000000953674316px_2.4000000953674316px_0px_rgba(0,0,0,0.25)] outline outline-[2.40px] outline-offset-[-2.40px] outline-blue-600 inline-flex flex-col justify-center items-center gap-9 overflow-hidden">
          <RegisterSign />
          <Email />
          <div
            data-property-1="Default"
            className="w-96 h-12 px-14 py-9 bg-blue-600 rounded-[50.88px] shadow-[0px_0px_12.720000267028809px_3.180000066757202px_rgba(8,119,246,1.00)] inline-flex justify-center items-center gap-8 overflow-hidden"
          >
            <div className="justify-start text-white text-3xl font-bold font-['Inter'] [text-shadow:_13px_13px_13px_rgb(0_0_0_/_0.25)]">
              Register
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
