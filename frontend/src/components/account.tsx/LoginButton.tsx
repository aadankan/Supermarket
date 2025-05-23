const LoginButton = (props: {login: () => void}) => {
  return (
    <div
      className="h-24 px-11 py-7 bg-amber-500 rounded-[40.60px] shadow-[0px_0px_10px_2.5px_rgba(232,158,0,1.00)] inline-flex justify-center items-center gap-6 overflow-hidden cursor-pointer"
      onClick={props.login}
    >
      <div className="justify-start text-white text-4xl font-bold [text-shadow:_10px_10px_10px_rgb(0_0_0_/_0.25)]">
        Log In
      </div>
    </div>
  );
};

export default LoginButton