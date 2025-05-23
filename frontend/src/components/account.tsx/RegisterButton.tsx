const RegisterButton = (props: {register: () => void}) => {
  return (
    <div
          className="h-24 px-11 py-7 bg-blue-600 rounded-[40px] shadow-[0px_0px_10px_2.5px_rgba(8,119,246,1.00)] inline-flex justify-center items-center gap-6 overflow-hidden cursor-pointer"
          onClick={props.register}
        >
          <div className="justify-start text-white text-4xl font-bold [text-shadow:_10px_10px_10px_rgb(0_0_0_/_0.25)]">
            Register
          </div>
        </div>
  )
}

export default RegisterButton;