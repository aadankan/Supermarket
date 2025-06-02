import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import supermarket from "../../assets/images/SupermarketEntrance.png";
import AdminPanel from "../../components/account.tsx/AdminPanel";
import RegisterSign from "../../components/account.tsx/RegisterSign";
import LoginButton from "../../components/account.tsx/LoginButton";
import RegisterButton from "../../components/account.tsx/RegisterButton";
import CheckEmail from "../../components/account.tsx/CheckEmail";
import Password from "../../components/account.tsx/Password";
import ConfirmPassword from "../../components/account.tsx/ConfirmPassword";
import LabelAndInput from "../../components/account.tsx/LabelAndInput";

const RegisterPage = () => {
  const navigate = useNavigate();
  const [emailConfirmed, setEmailConfirmed] = useState(() => {
    return JSON.parse(sessionStorage.getItem("emailConfirmed") || "false");
  });

  const [emailConfirmPage, setEmailConfirmPage] = useState(() => {
    return JSON.parse(sessionStorage.getItem("emailConfirmPage") || "false");
  });

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordMatch, setPasswordMatch] = useState(false);
  const [username, setUsername] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [usernameChecked, setUsernameChecked] = useState(false);
  const [phoneNumber, setPhoneNumber] = useState("");
  const [country, setCountry] = useState("");
  const [postalCode, setPostalCode] = useState("");
  const [city, setCity] = useState("");
  const [street, setStreet] = useState("");

  const login = () => {
    navigate("/login");
  };

  const register = async () => {
    try {
      const registerResponse = await fetch("http://localhost:8000/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      if (!registerResponse.ok) {
        const errorData = await registerResponse.json();
        throw new Error(errorData.detail || "Failed to register user");
      }

      const emailResponse = await fetch("http://localhost:8000/email-verification/send-verification", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      if (!emailResponse.ok) {
        const errorData = await emailResponse.json();
        throw new Error(errorData.detail || "Failed to send verification email");
      }

      setEmailConfirmPage(true);
    } catch (error) {
      console.error("Error during registration or sending email verification:", error);
      if (error instanceof Error) {
        alert(error.message);
      } else {
        alert("An unknown error occurred.");
      }
    }
  };

  const getUserId = async () => {
    try {
      const response = await fetch("http://localhost:8000/users/get-user-id", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to get user ID");
      }

      const data = await response.json();
      return data.userId;
    } catch (error) {
      console.error("Error getting user ID:", error);
      if (error instanceof Error) {
        alert(error.message);
      } else {
        alert("An unknown error occurred.");
      }
      return null;
    }
  };

  const registerUser = async () => {
    const userId = await getUserId();
    console.log("userId", userId);

    if (!userId) {
      alert("User ID is missing. Please restart the registration process.");
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/users/${userId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          password,
          username,
          firstName,
          lastName,
          phoneNumber,
          country,
          postalCode,
          city,
          street,
          is_admin: false
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Validation errors:", errorData);
        throw new Error(JSON.stringify(errorData.detail) || "Failed to update user");
      }

      alert("User registered successfully");
      navigate("/login");
    } catch (error) {
      console.error("Error during user registration:", error);
      if (error instanceof Error) {
        alert(error.message);
      } else {
        alert("An unknown error occurred.");
      }
    }
  };

  const passwordCheck = () => {
    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }
    if (password.length < 8) {
      alert("Password must be at least 8 characters long");
      return;
    }
    if (!/[A-Z]/.test(password)) {
      alert("Password must contain at least one uppercase letter");
      return;
    }

    setPasswordMatch(true);
  };

  const usernameCheck = async () => {
    if (!username) {
      alert("Username is required");
      return;
    }
    if (!firstName) {
      alert("First name is required");
      return;
    }
    if (!lastName) {
      alert("Last name is required");
      return;
    }

    setUsernameChecked(true);
  };

  useEffect(() => {
    sessionStorage.setItem("emailConfirmed", JSON.stringify(emailConfirmed));
  }, [emailConfirmed]);

  useEffect(() => {
    sessionStorage.setItem("emailConfirmPage", JSON.stringify(emailConfirmPage));
  }, [emailConfirmPage]);

  useEffect(() => {
    if (emailConfirmed) {
      setEmailConfirmPage(false);
    }
  }, [emailConfirmed]);

  useEffect(() => {
    console.log("emailConfirmed", emailConfirmed);

    const checkEmailConfirmed = async () => {
      try {
        if (!email) return;

        const response = await fetch("http://localhost:8000/email-verification/check-email-confirmed", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email }),
        });

        if (!response.ok) throw new Error("Failed to check email confirmation");

        const data = await response.json();
        console.log("Check email confirmed response:", data);
        setEmailConfirmed(data.emailConfirmed);
      } catch (error) {
        console.error("Error checking email confirmation:", error);
      }
    };

    if (emailConfirmPage) {
      const interval = setInterval(checkEmailConfirmed, 5000);
      return () => clearInterval(interval);
    }
  }, [emailConfirmPage, email]);

  sessionStorage.removeItem("emailConfirmed");
  sessionStorage.removeItem("emailConfirmPage");

  return (
    <div style={{ backgroundImage: `url(${supermarket})` }} className="bg-cover bg-bottom h-screen">
      <div className="w-full h-full flex justify-center items-center gap-40 overflow-hidden">
        <div className="p-10 bg-white/60 rounded-[48px] shadow-[0px_2.4000000953674316px_2.4000000953674316px_0px_rgba(0,0,0,0.25)] outline-4 outline-blue-600 inline-flex flex-col justify-center items-center gap-7 overflow-hidden">
          <RegisterSign />
          {!emailConfirmPage && !emailConfirmed && (
            <div>
              <div className="w-full flex flex-col justify-center items-center gap-4">
                <LabelAndInput
                  center={true}
                  inputType="text"
                  placeholderText="test@example.com"
                  labelText="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                <div className="w-[80%]">
                  <RegisterButton register={register} fullWidth={true}>
                    <div className="justify-start text-white text-3xl font-bold">Register</div>
                  </RegisterButton>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-xl text-white font-['Inter'] [text-shadow:_2px_2px_2px_rgb(0_0_0_/_0.5)]">
                    You already have an account?
                  </div>
                  <LoginButton login={login}>
                    <div className="justify-start text-white text-xl font-bold cursor-pointer">Log In</div>
                  </LoginButton>
                </div>
              </div>
            </div>
          )}

          {!emailConfirmed && emailConfirmPage && <CheckEmail email={email} />}

          {emailConfirmed && !passwordMatch && (
            <div className="w-full flex flex-col justify-center items-center gap-6">
              <div className="text-3xl text-white font-bold [text-shadow:_0px_0px_4px_rgb(0_0_0_/_1)]">
                Email verified correctly
              </div>
              <div className={`flex flex-col items-start gap-3.5 overflow-hidden`}>
                <LabelAndInput
                  inputType="password"
                  placeholderText="Pasword"
                  labelText="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <LabelAndInput
                  inputType="password"
                  placeholderText="Pasword"
                  labelText="Confirm your password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </div>
              <div className="w-[80%]">
                <RegisterButton register={passwordCheck} fullWidth={true}>
                  <div className="justify-start text-white text-3xl font-bold">Continue</div>
                </RegisterButton>
              </div>
            </div>
          )}

          {passwordMatch && !usernameChecked && (
            <div className="w-full flex flex-col justify-center items-center gap-4">
              <div className={`flex flex-col items-start gap-3.5 overflow-hidden`}>
                <LabelAndInput
                  inputType="text"
                  placeholderText="Username"
                  labelText="Enter your username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
                <LabelAndInput
                  inputType="text"
                  placeholderText="First Name"
                  labelText="Enter your first name"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                />
                <LabelAndInput
                  inputType="text"
                  placeholderText="Last Name"
                  labelText="Enter your last name"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                />
              </div>
              <div className="w-[80%]">
                <RegisterButton register={usernameCheck} fullWidth={true}>
                  <div className="justify-start text-white text-3xl font-bold">Continue</div>
                </RegisterButton>
              </div>
            </div>
          )}

          {usernameChecked && (
            <div className="w-full flex flex-col justify-center items-center gap-4">
              <div className={`max-h-60 flex flex-col items-start gap-3.5 overflow-auto`}>
                <LabelAndInput
                  inputType="text"
                  placeholderText="Phone Number"
                  labelText="Enter your phone number"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                />
                <LabelAndInput
                  inputType="text"
                  placeholderText="Country"
                  labelText="Enter your country"
                  value={country}
                  onChange={(e) => setCountry(e.target.value)}
                />
                <LabelAndInput
                  inputType="text"
                  placeholderText="Postal Code"
                  labelText="Enter your postal code"
                  value={postalCode}
                  onChange={(e) => setPostalCode(e.target.value)}
                />
                <LabelAndInput
                  inputType="text"
                  placeholderText="City"
                  labelText="Enter your city"
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                />
                <LabelAndInput
                  inputType="text"
                  placeholderText="Street"
                  labelText="Enter your street"
                  value={street}
                  onChange={(e) => setStreet(e.target.value)}
                />
              </div>
              <div className="w-[80%]">
                <RegisterButton register={registerUser} fullWidth={true}>
                  <div className="justify-start text-white text-3xl font-bold">Register</div>
                </RegisterButton>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
