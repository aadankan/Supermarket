const LoginButton = (props: {login: () => void, children: any, fullWidth?: boolean}) => {
  return (
    <div
      className={`${props.fullWidth&&"w-full"} px-5 py-2 bg-amber-500 rounded-full shadow-lg shadow-amber-500 inline-flex justify-center items-center gap-6 overflow-hidden cursor-pointer`}
      onClick={props.login}
    >
      {props.children}
    </div>
  );
};

export default LoginButton