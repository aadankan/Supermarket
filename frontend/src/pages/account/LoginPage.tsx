import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import supermarket from "../../assets/images/SupermarketEntrance.png";
import LoginButton from "../../components/account.tsx/LoginButton";
import LabelAndInput from "../../components/account.tsx/LabelAndInput";

const LoginPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    try {
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Login failed");
      }

      const data = await response.json();
      const { access_token } = data;

      // Zapisz token do localStorage
      localStorage.setItem("token", access_token);

      // Przekierowanie po zalogowaniu
      navigate("/");
    } catch (error) {
      console.error("Login error:", error);
      if (error instanceof Error) {
        alert("Login failed: " + error.message);
      } else {
        alert("Login failed: " + String(error));
      }
    }
  };

  const register = () => {
    navigate("/register");
  };

  return (
    <div style={{ backgroundImage: `url(${supermarket})` }} className="bg-cover bg-bottom h-screen">
      <div className="w-full h-full flex justify-center items-center overflow-hidden">
        <div className="p-9 bg-white/60 rounded-[60px] shadow-[0px_3px_3px_0px_rgba(0,0,0,0.25)] outline-4 outline-blue-600 inline-flex flex-col justify-center items-center gap-8 overflow-hidden">
          <div className="w-full flex flex-col justify-center items-center gap-4 overflow-hidden">
            <LabelAndInput
              inputType="text"
              placeholderText="test@example.com"
              labelText="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <LabelAndInput
              inputType="password"
              placeholderText="Password"
              labelText="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  login();
                }
              }}
            />
          </div>
          <div className="w-[80%]">
            <LoginButton login={login} fullWidth={true}>
              <div className="justify-start text-white text-3xl font-bold [text-shadow:_16px_16px_16px_rgb(0_0_0_/_0.25)]">
                Log In
              </div>
            </LoginButton>
          </div>
          <div className="flex items-center gap-3">
            <div className="text-xl text-white [text-shadow:_0px_3px_3px_rgb(0_0_0_/_1)]">
              You don't have an account?
            </div>
            <div
              className="h-14 p-3 bg-blue-600 rounded-[63.60px] shadow-[0px_0px_15.899999618530273px_3.9749999046325684px_rgba(8,119,246,1.00)] inline-flex justify-center items-center gap-10 overflow-hidden"
              onClick={register}
            >
              <div className="justify-start text-white text-xl font-bold [text-shadow:_16px_16px_16px_rgb(0_0_0_/_0.25)] cursor-pointer">
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
