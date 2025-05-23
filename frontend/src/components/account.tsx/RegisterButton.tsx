const RegisterButton = (props: { register: () => void; children: any; fullWidth?: boolean }) => {
  return (
    <div
      className={`${
        props.fullWidth && "w-full"
      } px-5 py-2 bg-blue-600 rounded-[40px] shadow-lg shadow-blue-600 inline-flex justify-center items-center gap-6 overflow-hidden cursor-pointer`}
      onClick={props.register}
    >
      {props.children}
    </div>
  );
};

export default RegisterButton;
