import { useNavigate } from "react-router-dom";
import supermarket from "../../assets/images/SupermarketEntrance.png";
import AdminPanel from "../../components/account.tsx/AdminPanel";
import Email from "../../components/account.tsx/Email";
import Password from "../../components/account.tsx/Password";

const LoginPage = () => {
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
        <div className="w-[40%] p-9 bg-white/60 rounded-[60px] shadow-[0px_3px_3px_0px_rgba(0,0,0,0.25)] outline outline-[3px] outline-offset-[-3px] outline-blue-600 inline-flex flex-col justify-center items-center gap-11 overflow-hidden">
          <Email />
          <Password />
          <div className="w-[80%] h-14 px-4 py-11 bg-amber-500 rounded-[63.60px] shadow-[0px_0px_6.5px_2px_rgba(232,158,0,50)] inline-flex justify-center items-center gap-10 overflow-hidden">
            <div className="justify-start text-white text-4xl font-bold [text-shadow:_16px_16px_16px_rgb(0_0_0_/_0.25)]">
              Log In
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="text-xl text-white [text-shadow:_0px_3px_3px_rgb(0_0_0_/_1)]">
              You don't have an account?
            </div>
            <div
              className="h-14 p-6 bg-blue-600 rounded-[63.60px] shadow-[0px_0px_15.899999618530273px_3.9749999046325684px_rgba(8,119,246,1.00)] inline-flex justify-center items-center gap-10 overflow-hidden"
              onClick={register}
            >
              <div className="justify-start text-white text-2xl font-bold [text-shadow:_16px_16px_16px_rgb(0_0_0_/_0.25)] cursor-pointer">
                Registration
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
